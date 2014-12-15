

import os

from osp.corpus.syllabus import Syllabus
from functools import lru_cache


class Segment:


    def __init__(self, path):

        """
        Initialize the segment reader.

        :param path: The segment path.
        """

        self.path = os.path.abspath(path)


    @property
    @lru_cache()
    def file_names(self):

        """
        Get a list of all syllabus file names.
        """

        names = []
        for name in os.listdir(self.path):

            # Ignore `.log` files.
            if os.path.splitext(name)[1] != '.log':
                names.append(name)

        return names


    @property
    @lru_cache()
    def file_count(self):

        """
        How many syllabi are contained in the segment?
        """

        return len(self.file_names)


    def file_paths(self):

        """
        Generate fully qualified paths for each file.
        """

        for name in self.file_names:
            yield os.path.join(self.path, name)


    def syllabi(self):

        """
        Generate Syllabus instances for each file.
        """

        for path in self.file_paths():
            yield Syllabus(path)
