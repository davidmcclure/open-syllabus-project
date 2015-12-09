

import os

from osp.common.config import config
from osp.common.utils import grouper
from osp.citations.segment import Segment


class HLOM_Corpus:


    @classmethod
    def from_env(cls):

        """
        Get an instance for the ENV-defined corpus.
        """

        return cls(config['hlom']['corpus'])


    def __init__(self, path):

        """
        Set the dataset path.

        Args:
            path (str): A relative path to the dataset.
        """

        self.path = os.path.abspath(path)


    def segments(self):

        """
        Generate `Segment` instances for each directory.
        """

        for name in os.listdir(self.path):
            yield Segment(os.path.join(self.path, name))


    def records(self):

        """
        Generate `Record` instances for record file in the dataset.
        """

        for segment in self.segments():
            for record in segment.records():
                yield record


    def grouped_records(self, n):

        """
        Generate groups of N records.

        Args:
            n (int): The group length.
        """

        for segment in self.segments():
            for group in grouper(segment.records(), n):
                yield group
