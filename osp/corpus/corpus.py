

import os

from osp.common.config import config
from osp.corpus.segment import Segment
from osp.corpus.utils import int_to_dir
from functools import lru_cache
from clint.textui.progress import bar


class Corpus:


    @classmethod
    def from_env(cls, **kwargs):

        """
        Get an instance for the ENV-defined corpus.
        """

        return cls(config['osp']['corpus'], **kwargs)


    def __init__(self, path, s1=0, s2=4095):

        """
        Set the path and segment boundaries.

        :param path: A relative path to the corpus.
        :param s1: The first segment.
        :param s2: The last segment.
        """

        self.path = os.path.abspath(path)
        self.s1 = s1
        self.s2 = s2


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

        for s in range(self.s1, self.s2):

            # Get the segment directory path.
            path = os.path.join(self.path, int_to_dir(s))

            # Only yield segment if the path exists.
            if os.path.exists(path): yield Segment(path)


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


    def syllabi_bar(self):

        """
        Wrap the syllabi iterator in a progress bar.
        """

        size = self.file_count
        for syllabus in bar(self.syllabi(), expected_size=size):
            yield syllabus
