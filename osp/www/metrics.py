

from redis import StrictRedis
from scipy.stats import rankdata

from osp.common import config
from osp.citations.models import Citation_Index


class Metrics:


    def __init__(self):

        """
        Connect to Redis.
        """

        self.redis = StrictRedis(**config['redis'])


    def index_counts(self):

        """
        Index the raw text counts.
        """

        counts = Citation_Index.compute_ranking()

        # Text -> total count.
        self.redis.hmset('osp-counts', counts)


    def count(self, text_id):

        """
        Get the citation count for a text.

        Args:
            text_id (int)

        Returns: int
        """

        count = self.redis.hget('osp-counts', text_id)

        return int(count) if count else None
