

import os
import logging

from osp.common.config import config
from redis import StrictRedis
from playhouse.postgres_ext import PostgresqlExtDatabase
from elasticsearch import Elasticsearch
from peewee import *


# Elasticsearch.
elasticsearch = Elasticsearch([
    config['elasticsearch']
])

# Redis.
redis = StrictRedis(**config['redis'])

# Dial down Elasticsearch logging.
logging.getLogger('elasticsearch.trace').propagate = False
