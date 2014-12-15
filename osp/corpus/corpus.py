

import os

from osp.corpus.segment import Segment
from functools import lru_cache


class Corpus:


    def __init__(self, path):

        """
        Initialize the segment reader.

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
