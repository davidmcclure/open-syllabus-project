

import os

from osp.common.config import config
from osp.corpus.segment import Segment
from osp.corpus.utils import int_to_dir
from functools import lru_cache
from clint.textui import progress


class Corpus:


    @classmethod
    def from_env(cls):

        """
        Get an instance for the ENV-defined corpus.
        """

        return cls(config['osp']['corpus'])


    def __init__(self, path):

        """
        Set the path and segment boundaries.

        :param path: A relative path to the corpus.
        """

        self.path = os.path.abspath(path)


    @property
    @lru_cache()
    def file_count(self):

        """
        How many syllabi are contained in the entire corpus?
        """

        count = 0
        for segment in self.segments():
            count += segment.file_count

        return count


    def segments(self):

        """
        Generate `Segment` instances for each directory.
        """

        for name in os.listdir(self.path):
            yield Segment(os.path.join(self.path, name))


    def file_paths(self):

        """
        Generate fully qualified paths for every file in the corpus.
        """

        for segment in self.segments():
            for path in segment.file_paths():
                yield path


    def syllabi(self):

        """
        Generate `Syllabus` instances for every file in the corpus.
        """

        for segment in self.segments():
            for syllabus in segment.syllabi():
                yield syllabus


    def cli_syllabi(self):

        """
        Wrap the syllabi iterator in a progress bar.
        """

        n = self.file_count
        for syllabus in progress.bar(self.syllabi(), expected_size=n):
            yield syllabus
