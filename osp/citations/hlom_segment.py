

import os

from pymarc import MARCReader


class HLOM_Segment:


    def __init__(self, path):

        """
        Initialize the segment reader.

        Args:
            path (str): The segment path.
        """

        self.path = os.path.abspath(path)


    def records(self):

        """
        Generate record instances.
        """

        with open(self.path, 'rb') as fh:

            reader = MARCReader(fh,
                ascii_handling='ignore',
                utf8_handling='ignore',
            )

            for record in reader:
                yield record
