

import os
import tempfile
import datetime
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


    def add_file(self, content='content', name=None, segment='000',
                 ftype='plain', log={}):

        """
        Add a file to the corpus.

        Args:
            content (str): The file content.
            name (str): The file name.
            segment (str): The segment name.
            ftype (str): The file type.
            log (dict): Custom log data.

        Returns:
            str: The path of the new file.
        """

        self.add_segment(segment)

        # Hash the content, if no name.
        if not name:
            sha1 = hashlib.sha1()
            sha1.update(content.encode('utf8'))
            name = sha1.hexdigest()

        # Get the complete path.
        path = os.path.join(self.dir, segment+'/'+name)

        # Write the file.
        write_file = getattr(self, '_write_'+ftype)
        write_file(path, content)
        self.write_log(path, ftype, log)

        return path


    def write_log(self, path, ftype, log={}):

        """
        Write a .log file.

        Args:
            path (str): The file path.
            ftype (str): The file type.
            log (dict): Custom log data.
        """

        metadata = {
            'url':          'http://opensyllabusproject.org',
            'provenance':   'osp-test',
            'date':         datetime.datetime.now().isoformat(),
            'checksum':     os.path.basename(path),
            'format':       ftype
        }

        metadata.update(log)

        order = [
            'url',
            'provenance',
            'date',
            'checksum',
            'format'
        ]

        # Write the log.
        with open(path+'.log', 'w+') as fh:
            for key in order:
                print(metadata[key], file=fh)


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
