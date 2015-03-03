

import logging

from osp.common.config import config
from redis import StrictRedis
from elasticsearch import Elasticsearch


# REDIS
redis = StrictRedis(**config['redis'])

# ELASTICSEARCH
elasticsearch = Elasticsearch([
    config['elasticsearch']
])

# Dial down Elasticsearch logging.
logging.getLogger('elasticsearch.trace').propagate = False
