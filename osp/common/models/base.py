

import os
import logging

from osp.common.config import config
from redis import StrictRedis
from playhouse.postgres_ext import PostgresqlExtDatabase
from elasticsearch import Elasticsearch
from peewee import *


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
