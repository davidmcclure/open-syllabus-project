

import os
import anyconfig
import copy
import logging

from playhouse.postgres_ext import PostgresqlExtDatabase
from rq import Queue
from elasticsearch import Elasticsearch
from redis import StrictRedis
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


# Throttle logging.
logging.getLogger('elasticsearch.trace').propagate = False
anyconfig.set_loglevel('WARNING')


class Config:


    @classmethod
    def from_env(cls):

        """
        Get a config instance with the default file precedence.
        """

        return cls([
            os.path.join(os.path.dirname(__file__), 'osp.yml'),
            '/etc/osp/osp.yml',
        ])


    def __init__(self, paths):

        """
        Initialize the configuration object.

        Args:
            paths (list): YAML paths, from the most to least specific.
        """

        self.paths = paths
        self.read()


    def __getitem__(self, key):

        """
        Get a configuration value.

        Args:
            key (str): The configuration key.

        Returns:
            The option value.
        """

        return self.config.get(key)


    def read(self):

        """
        Load the configuration files, set connections.
        """

        self.config = anyconfig.load(self.paths, ignore_missing=True)

        # Elasticsearch
        self.es = self.build_es()

        # Redis
        self.redis = self.build_redis()

        # Queue
        self.rq = self.build_rq()


    def build_db(self, name='default'):

        """
        Get a Postgres database object.

        Args:
            name (str): The database key.

        Returns:
            The database object.
        """

        defaults = self['postgres']['default']['args']

        db = (
            self['postgres']
            .get(name, {})
            .get('args', {})
        )

        args = dict(
            list(defaults.items()) +
            list(db.items())
        )

        return PostgresqlExtDatabase(
            autorollback=True,
            register_hstore=False,
            **args
        )


    def build_table_db(self, table):

        """
        Get a Postgres database object for a table name.

        Args:
            table (str): The name of the table.

        Returns:
            The database object.
        """

        name = None

        # Try to find a custom host.
        for key, db in self['postgres'].items():
            if table in db.get('tables', {}):
                name = key

        return self.build_db(name)


    def build_es(self):

        """
        Get an Elasticsearch connection.

        Returns:
            Elasticsearch
        """

        if 'elasticsearch' in self.config:
            return Elasticsearch([self['elasticsearch']])


    def build_redis(self):

        """
        Get a Redis connection.

        Returns:
            StrictRedis
        """

        if 'redis' in self.config:
            return StrictRedis(**self['redis'])


    def build_rq(self):

        """
        Get an RQ instance.

        Returns:
            rq.Queue
        """

        redis = self.build_redis()

        if redis:
            return Queue(connection=redis)


    def build_engine(self):

        """
        Build an SQLAlchemy engine.

        Returns: Engine
        """

        return create_engine(URL(**self['sqlalchemy']))


    def build_sessionmaker(self):

        """
        Build an SQLAlchemy session class.

        Returns: sessionmaker
        """

        return sessionmaker(bind=self.build_engine())


    def build_session(self):

        """
        Get a database session.

        Returns: Session
        """

        Session = self.build_sessionmaker()

        return Session()


    @contextmanager
    def transaction(self):

        """
        Provide a transactional scope around a query.

        Yields: Session
        """

        session = self.build_session()

        try:
            yield session
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()


    def is_test(self):

        """
        Are we running inside of a test?

        Returns: bool
        """

        return bool(self.config.get('test'))
