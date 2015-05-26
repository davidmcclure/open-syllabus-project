

import csv

from osp.common.config import config
from nltk.stem import PorterStemmer


class Counts:


    def __init__(self):

        """
        Read the csv, index counts / ranks.
        """

        self.stem   = PorterStemmer().stem
        self.counts = {}
        self.ranks  = {}

        with open(config['osp']['counts']) as fh:

            reader = csv.DictReader(fh)

            for i, row in enumerate(reader):
                self.counts[row['term']] = row['count']
                self.ranks[row['term']] = i


    def count(self, term):

        """
        Get a term's frequency count.

        Args:
            term (str): An unstemmed term.

        Returns: int
        """

        return self.counts.get(self.stem(term))


    def rank(self, term):

        """
        Get a term's frequency rank.

        Args:
            term (str): An unstemmed term.

        Returns: int
        """

        return self.ranks.get(self.stem(term))
