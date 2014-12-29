

import os

from osp.corpus.segment import Segment
from osp.corpus.utils import int_to_dir
from functools import lru_cache
from clint.textui import progress


class Group:


    def __init__(self, path, s1=0, s2=4095):

        """
        Initialize the segment reader.

        :param path: A relative path to the corpus.
        :param s1: The first segment.
        :param s2: The last segment.
        """

        self.path = os.path.abspath(path)
        self.s1 = s1
        self.s2 = s2


    def segments(self):

        """
        Generate `Segment` instances for each directory.
        """

        for s in range(self.s1, self.s2):
            yield Segment(os.path.join(self.path, int_to_dir(s)))
