

import os
import logging

from redis import StrictRedis
from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import *
from elasticsearch import Elasticsearch
from osp.common.config import config


# Local (worker) database.
pg_local = PostgresqlExtDatabase(
    server_side_cursors=True,
    **config['postgres']['local']
)

# Remote (server) database.
pg_remote = PostgresqlExtDatabase(
    server_side_cursors=True,
    **config['postgres']['remote']
)

# ELASTICSEARCH
elasticsearch = Elasticsearch([config['elasticsearch']])
logging.getLogger('elasticsearch.trace').propagate = False

# REDIS
redis = StrictRedis(**config['redis'])


class LocalModel(Model):
    class Meta:
        database = pg_local


class RemoteModel(Model):
    class Meta:
        database = pg_remote
