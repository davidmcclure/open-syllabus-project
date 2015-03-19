

import logging
import datetime

from osp.common.config import config
from peewee import Model, DateTimeField, fn
from rq import Queue
from redis import StrictRedis


# REDIS/RQ
redis = StrictRedis(**config['redis'])
queue = Queue(connection=redis)


class BaseModel(Model):
    created = DateTimeField(default=datetime.datetime.now)
