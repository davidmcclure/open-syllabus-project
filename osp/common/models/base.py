

import os

from redis import StrictRedis
from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import *
from elasticsearch import Elasticsearch
from osp.common.config import config


# POSTGRES
pg_local  = PostgresqlExtDatabase(**config['postgres']['local'])
pg_remote = PostgresqlExtDatabase(**config['postgres']['remote'])

# REDIS
redis = StrictRedis(**config['redis'])

# ELASTICSEARCH
elasticsearch = Elasticsearch([config['elasticsearch']])


class LocalModel(Model):
    class Meta:
        database = pg_local


class RemoteModel(Model):
    class Meta:
        database = pg_remote
