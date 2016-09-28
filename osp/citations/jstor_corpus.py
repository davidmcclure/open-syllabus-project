

import scandir
import os

from osp.common import config
from osp.citations.jstor_record import JSTOR_Record


class JSTOR_Corpus:

    @classmethod
    def from_env(cls):

        """
        Get an instance for the ENV-defined corpus.
        """

        return cls(config['jstor']['corpus'])

    def __init__(self, path):

        """
        Set the corpus path.

        Args:
            path (str): A relative path to the dataset.
        """

        self.path = os.path.abspath(path)

    def paths(self):

        """
        Generate XML manifest paths.
        """

        for root, dirs, files in scandir.walk(self.path):

            # Filter out non-XML files.
            xmls = [
                n for n in files
                if os.path.splitext(n)[-1] == '.xml'
            ]

            for name in xmls:
                yield os.path.join(root, name)

    def texts(self):

        """
        Generate text mappings.
        """

        for path in self.paths():

            try:

                record = JSTOR_Record(path)

                if record.is_queryable():
                    yield record.text()

            except Exception as e:
                print(e)
