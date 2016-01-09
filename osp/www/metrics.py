

from redis import StrictRedis

from osp.common.config import config


class Metrics:


    def __init__(self):

        """
        Connect to Redis.
        """

        self.redis = StrictRedis(**config['redis'])
