

import os

from osp.corpus.syllabus import Syllabus
from cached_property import cached_property


class Segment:


    def __init__(self, path):

        """
        Initialize the segment reader.

        Args:
            path (str): The segment path.
        """

        self.path = os.path.abspath(path)


    def file_names(self):

        """
        Get a list of all syllabus file names.

        Yields:
            str: The next file name.
        """

        for name in sorted(os.listdir(self.path)):

            # Ignore `.log` files.
            if os.path.splitext(name)[1] != '.log':
                yield name


    @cached_property
    def file_count(self):

        """
        How many syllabi are contained in the segment?

        Returns:
            int: The number of syllabi.
        """

        return sum(1 for _ in self.file_names())


    def file_paths(self):

        """
        Generate fully qualified paths for each file.

        Yields:
            str: The next file path.
        """

        for name in self.file_names():
            yield os.path.join(self.path, name)


    def syllabi(self):

        """
        Generate Syllabus instances for each file.

        Yields:
            Syllabus: The next syllabus.
        """

        for path in self.file_paths():
            yield Syllabus(path)
