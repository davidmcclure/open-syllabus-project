

import os
import tempfile


class MockCorpus:


    def __init__(self):
        """
        Create the temporary directory.
        """
        self.dir = tempfile.mkdtemp()


    def add_segment(self, name):
        """
        Create a segment directory.

        :param name: The segment name.
        """
        path = os.path.join(self.dir, name)

        if not os.path.exists(path):
            os.makedirs(path)
