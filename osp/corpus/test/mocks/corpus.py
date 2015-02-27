

import os
import tempfile
import hashlib

from abc import ABCMeta
from reportlab.pdfgen.canvas import Canvas
from docx import Document


class MockCorpus:


    def __init__(self):

        """
        Create the temporary directory.
        """

        self.dir = tempfile.mkdtemp()


    def add_segment(self, name):

        """
        Add a segment directory, if it doesn't exist.

        Args:
            name (str): The segment name.
        """

        path = os.path.join(self.dir, name)

        if not os.path.exists(path):
            os.makedirs(path)


    def add_file(self, content, segment='000', ftype='plain'):

        """
        Add a file to the corpus.

        Args:
            segment (str): The segment name.
            content (str): The file content.
            ftype (str): The file type.

        Returns:
            str: The path of the new file.
        """

        self.add_segment(segment)

        # Get the file checksum.
        sha1 = hashlib.sha1()
        sha1.update(content.encode('utf8'))
        name = sha1.hexdigest()

        # Get the complete path.
        path = os.path.join(self.dir, segment+'/'+sha1.hexdigest())

        # Write the file.
        write_file = getattr(self, '_write_'+ftype)
        write_file(path, content)

        return path


    def _write_plain(self, path, content):

        """
        Write a plaintext file.

        Args:
            path (str): The file path.
            content (str): The file content.
        """

        with open(path, 'w+') as fh:
            fh.write(content)


    def _write_pdf(self, path, content):

        """
        Write a .pdf file.

        Args:
            path (str): The file path.
            content (str): The file content.
        """

        canvas = Canvas(path)
        canvas.drawString(12, 720, content)
        canvas.save()


    def _write_docx(self, path, content):

        """
        Write a .docx file.

        Args:
            path (str): The file path.
            content (str): The file content.

        Returns:
            file: A handle on the new file.
        """

        docx = Document()
        docx.add_paragraph(content)
        docx.save(path)
