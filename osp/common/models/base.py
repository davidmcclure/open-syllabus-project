

import os

from redis import StrictRedis
from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import *
from elasticsearch import Elasticsearch
from osp.common.config import config


# POSTGRES
postgres = PostgresqlExtDatabase(**config['postgres'])

# REDIS
redis = StrictRedis(**config['redis'])

# ELASTICSEARCH
elasticsearch = Elasticsearch([config['elasticsearch']])


class BaseModel(Model):
    class Meta:
        database = postgres
