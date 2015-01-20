

import os

from pymarc import MARCReader


class Segment:


    def __init__(self, path):

        """
        Initialize the segment reader.

        :param path: The segment path.
        """

        self.path = os.path.abspath(path)


    def records(self):

        """
        Generate record instances.
        """

        with open(self.path, 'rb') as fh:
            reader = MARCReader(fh, utf8_handling='ignore')
            for record in reader:
                yield record
