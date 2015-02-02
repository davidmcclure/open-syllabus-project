

import os

from redis import StrictRedis
from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import *
from elasticsearch import Elasticsearch
from osp.common.config import config


# POSTGRES
pg_worker = PostgresqlExtDatabase(**config['postgres']['worker'])
pg_server = PostgresqlExtDatabase(**config['postgres']['server'])

# REDIS
redis = StrictRedis(**config['redis'])

# ELASTICSEARCH
elasticsearch = Elasticsearch([config['elasticsearch']])


class WorkerModel(Model):
    class Meta:
        database = pg_worker


class ServerModel(Model):
    class Meta:
        database = pg_server
