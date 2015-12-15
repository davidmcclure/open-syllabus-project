

import os

from osp.common.config import config
from pymarc import MARCReader


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


    def records(self):

        """
        Generate Record instances from the MARC files.
        """

        for name in os.listdir(self.path):

            path = os.path.join(self.path, name)

            with open(path, 'rb') as fh:

                reader = MARCReader(fh,
                    ascii_handling='ignore',
                    utf8_handling='ignore',
                )

                for record in reader:
                    yield record
