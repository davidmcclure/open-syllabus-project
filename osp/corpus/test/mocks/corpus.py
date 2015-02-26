

import os
import tempfile

from abc import ABCMeta
from reportlab.pdfgen.canvas import Canvas
from docx import Document


class MockFile(metaclass=ABCMeta):

    @abstractmethod
    def write_file():
        pass

    def write_log():
        pass


class MockCorpus:


    def __init__(self):

        """
        Create the temporary directory.
        """

        self.dir = tempfile.mkdtemp()


    def add_segment(self, name):

        """
        Add a segment directory.

        Args:
            name (str): The segment name.
        """

        path = os.path.join(self.dir, name)

        if not os.path.exists(path):
            os.makedirs(path)


    def add_pdf(self, segment, name, content):

        """
        Add a PDF file.

        Args:
            segment (str): The segment name.
            name (str): The file name.
            content (str): The file content.

        Returns:
            file: A handle on the new file.
        """

        path = os.path.join(self.dir, segment+'/'+name)
        canvas = Canvas(path)

        canvas.drawString(12, 720, content)
        canvas.showPage()

        canvas.save()
        return open(path, 'rb')


    def add_docx(self, segment, name, content):

        """
        Add a .docx file.

        Args:
            segment (str): The segment name.
            name (str): The file name.
            content (str): The file content.

        Returns:
            file: A handle on the new file.
        """

        docx = Document()
        docx.add_paragraph(content)

        path = os.path.join(self.dir, segment+'/'+name)
        docx.save(path)

        return open(path, 'rb')
