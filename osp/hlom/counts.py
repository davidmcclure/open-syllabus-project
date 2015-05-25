

from osp.common.utils import read_csv
from nltk.stem import PorterStemmer


class Counts:


    def __init__(self):

        """
        Read the csv, index counts / ranks.
        """

        self.stem = PorterStemmer().stem

        self.reader = read_csv(
            'osp.citations.hlom',
            'data/counts.csv'
        )

        self.counts = {}
        self.ranks  = {}

        for i, row in enumerate(self.reader):
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
