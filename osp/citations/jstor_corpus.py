

import os
import scandir

from osp.common import config


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
            xmls = [n for n in files if os.path.splitext(n)[-1] == '.xml']

            for name in xmls:
                yield os.path.join(root, name)
