

import logging
import datetime

from osp.common.config import config
from peewee import Model, DateTimeField, fn
from redis import StrictRedis
from elasticsearch import Elasticsearch
from rq import Queue


# REDIS/RQ
redis = StrictRedis(**config['redis'])
queue = Queue(connection=redis)

# ELASTICSEARCH
elasticsearch = Elasticsearch([
    config['elasticsearch']
])

# Dial down Elasticsearch logging.
logging.getLogger('elasticsearch.trace').propagate = False


class BaseModel(Model):


    created = DateTimeField(default=datetime.datetime.now)


    @classmethod
    def max_id(cls):

        """
        Get the highest id in the table.
        """

        return cls.select(fn.max(cls.id)).scalar()
