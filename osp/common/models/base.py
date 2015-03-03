

import logging
import datetime

from osp.common.config import config
from redis import StrictRedis
from elasticsearch import Elasticsearch
from peewee import Model, DateTimeField


# REDIS
redis = StrictRedis(**config['redis'])

# ELASTICSEARCH
elasticsearch = Elasticsearch([
    config['elasticsearch']
])

# Dial down Elasticsearch logging.
logging.getLogger('elasticsearch.trace').propagate = False


class BaseModel(Model):
    created = DateTimeField(default=datetime.datetime.now)
