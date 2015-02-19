

import os
import logging

from redis import StrictRedis
from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import *
from elasticsearch import Elasticsearch
from osp.common.config import config


# Local (worker) database.
pg_local = PostgresqlExtDatabase(
    **config['postgres']['local']
)

# Remote (server) database.
pg_remote = PostgresqlExtDatabase(
    **config['postgres']['remote']
)

# Elasticsearch.
elasticsearch = Elasticsearch([
    config['elasticsearch']
])

# Redis.
redis = StrictRedis(**config['redis'])

# Dial down Elasticsearch logging.
logging.getLogger('elasticsearch.trace').propagate = False


class LocalModel(Model):
    class Meta:
        database = pg_local


class RemoteModel(Model):
    class Meta:
        database = pg_remote
