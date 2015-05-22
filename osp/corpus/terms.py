

import numpy as np
import requests

from osp.common.config import config
from collections import OrderedDict
from scipy.stats.mstats import zscore


class Terms:


    def __init__(self):

        """
        Load term frequencies, compute tf-idfs.
        """

        self._load_freqs()


    def _load_freqs(self):

        """
        Load frequency and document counts.
        """

        self.freqs = OrderedDict()
        self.zscores = OrderedDict()

        # TODO: Envi-fy.
        r = requests.get(
            'http://localhost:9200/hlom/_termlist?totalfreqs'
        )

        # Map the term -> count.
        for t in r.json()['terms']:
            self.freqs[t['name']] = t['totalfreq']

        # Compute zscores.
        zs = zscore(list(self.freqs.values()))

        # Map term -> zscore
        for i, t in enumerate(self.freqs.keys()):
            self.zscores[t] = zs[i]


    def validate_query(self, terms, threshold=0.1):

        """
        Does at least one term in a document query fall below a certain
        frequency threshold?

        Args:
            terms (set): The word types in the query.
            threshold (float): The max zscore.
        """

        for t in terms:
            if self.zscores[t] < threshold:
                return True

        return False
