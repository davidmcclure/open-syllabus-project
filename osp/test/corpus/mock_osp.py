

import os
import hashlib
import tempfile
import datetime
import shutil

from osp.corpus.utils import int_to_dir
from abc import ABCMeta
from reportlab.pdfgen.canvas import Canvas
from docx import Document
from datetime import datetime


class MockOSP:


    def __init__(self):

        """
        Create the temporary directory.
        """

        self.path = tempfile.mkdtemp()


    def add_segment(self, name):

        """
        Add a segment directory, if it doesn't exist.

        Args:
            name (str): The segment name.

        Returns:
            path (str): The path of the new segment.
        """

        path = os.path.join(self.path, name)
        if not os.path.exists(path): os.makedirs(path)
        return path


    def add_segments(self, s1=0, s2=4095):

        """
        Add a batch of segments, identified by an offset range.

        Args:
            s1 (int): The first segment.
            s2 (int): The last segment.
        """

        for i in range(s1, s2):
            self.add_segment(int_to_dir(i))


    def add_file(self, segment='000', name=None, content='content',
                 ftype='plain', log={}):

        """
        Add a file to the corpus.

        Args:
            segment (str): The segment name.
            name (str): The file name.
            content (str): The file content.
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
        path = os.path.join(self.path, segment+'/'+name)

        # Write the file and log.
        write_file = getattr(self, '_write_'+ftype)
        write_file(path, content)
        self.write_log(path, log)

        return path


    def add_files(self, segment, count, prefix='file-'):

        """
        Add a batch of files to a segment.

        Args:
            segment (str): The segment name.
            count (int): The number of files to add.
            prefix (str): A filename prefix.
        """

        for i in range(count):
            self.add_file(segment=segment, name=prefix+str(i))


    def write_log(self, path, log={}):

        """
        Write a .log file.

        Args:
            path (str): The file path.
            log (dict): Log overrides.
        """

        metadata = {
            'url':          'url',
            'provenance':   'provenance',
            'date':         'date',
            'checksum':     'checksum',
            'format':       'format'
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


    def _write_html(self, path, content):

        """
        Write an HTML file.

        Args:
            path (str): The file path.
            content (str): The file content.
        """

        with open(path, 'w+') as fh:
            fh.write('<html>'+content+'</html>')


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
        """

        docx = Document()
        docx.add_paragraph(content)
        docx.core_properties.created = datetime.now()
        docx.save(path)


    def teardown(self):

        """
        Delete the temporary directory.
        """

        shutil.rmtree(self.path)
