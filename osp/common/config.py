

import os
import anyconfig
import copy
import spacy.en
import logging

from playhouse.postgres_ext import PostgresqlExtDatabase
from rq import Queue
from elasticsearch import Elasticsearch
from redis import StrictRedis
from functools import lru_cache


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

        return self.config[key]


    def read(self):

        """
        Load the configuration files, set connections.
        """

        self.config = anyconfig.load(self.paths, ignore_missing=True)
        self.es = self.get_es()
        self.rq = self.get_rq()


    def get_db(self, name='default'):

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

        return PostgresqlExtDatabase(autorollback=True, **args)


    def get_table_db(self, table):

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

        return self.get_db(name)


    def get_es(self):

        """
        Get an Elasticsearch connection.

        Returns:
            elasticsearch.Elasticsearch
        """

        if 'elasticsearch' in self.config:
            return Elasticsearch([self['elasticsearch']])


    def get_rq(self):

        """
        Get an RQ instance.

        Returns:
            rq.Queue
        """

        if 'redis' in self.config:
            redis = StrictRedis(**self['redis'])
            return Queue(connection=redis)


    @lru_cache()
    def get_spacy(self):

        """
        Get a spaCy instance. Cache the result, to avoid reading in the data
        files more than once.

        Returns:
            spacy.en.English
        """

        return spacy.en.English()


# Global instance.
config = Config.from_env()
