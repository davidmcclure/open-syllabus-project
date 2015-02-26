

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
        Add a segment directory.

        :param name: The segment name.
        """
        path = os.path.join(self.dir, name)

        if not os.path.exists(path):
            os.makedirs(path)


    def add_pdf(self, segment, name, page_texts):
        """
        Add a PDF file.

        :param segment: The segment name.
        :param name: The file name.
        :param page_texts: A list of page texts.
        """
        pass
