

import os

from osp.common.config import config
from osp.citations.hlbd.segment import Segment
from osp.citations.hlbd.utils import groups


class Dataset:


    @classmethod
    def from_env(cls):

        """
        Get an instance for the ENV-defined corpus.
        """

        return cls(config['hlbd']['corpus'])


    def __init__(self, path):

        """
        Set the dataset path.

        :param path: A relative path to the dataset.
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

        :param n: The group length.
        """

        for segment in self.segments():
            for group in groups(segment.records(), n):
                yield group
