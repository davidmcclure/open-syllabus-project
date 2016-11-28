

import os
import tldextract
import re
import magic
import re

from osp.corpus import utils
from osp.common import config
from osp.common.utils import parse_domain
from contextlib import contextmanager
from cached_property import cached_property


# TODO: Don't use @property for the log methods.


class Syllabus:

    @classmethod
    def from_env(cls, relative_path):

        """
        Get an instance from a corpus-relative path.

        Args:
            relative_path (str): The corpus-relative path of the file.

        Returns:
            Syllabus: The wrapped instance.
        """

        path = os.path.join(config['osp']['corpus'], relative_path)
        return cls(path)

    def __init__(self, path):

        """
        Initialize a syllabus reader.

        Args:
            path (str): The file path.
        """

        self.path = os.path.abspath(path)

    def file_name(self):

        """
        Returns:
            str: The file name of the document.
        """

        return os.path.basename(self.path)

    def segment_name(self):

        """
        Returns:
            str: The name of the parent segment.
        """

        return os.path.split(os.path.dirname(self.path))[-1]

    def relative_path(self):

        """
        Returns:
            str: The file path, relative to the corpus.
        """

        return '/'.join([
            self.segment_name(),
            self.file_name(),
        ])

    @property
    def log_path(self):

        """
        Returns:
            str: The path of the corresponding log file.
        """

        return self.path+'.log'

    @property
    def log_exists(self):

        """
        Is the log file present?

        Returns:
            bool: True if the file exists.
        """

        return os.path.isfile(self.log_path)

    @cached_property
    def log(self):

        """
        Get the log file as an array of elements.

        Returns:
            list: Log elements.
        """

        if self.log_exists:
            with open(self.log_path, 'r', errors='ignore') as log:
                return log.read().splitlines()

        else: return []

    def metadata(self, offset):

        """
        Get a manifest element, identified by offset.

        Args:
            offset (int): The element offset.

        Returns:
            str|None: The metadata value.
        """

        if offset <= len(self.log)-1:
            return self.log[offset]

        else: return None

    def url(self):

        """
        Returns:
            str: The URL the file was scraped from.
        """

        return self.metadata(0)

    def provenance(self):

        """
        Returns:
            str: The origin of the file.
        """

        return self.metadata(1)

    def retrieved_date(self):

        """
        Returns:
            str: The date the file was scraped.
        """

        return self.metadata(2)

    def checksum(self):

        """
        Returns:
            str: The checksum for the file.
        """

        return self.metadata(3)

    def file_type(self):

        """
        Returns:
            str: The mime type of the file.
        """

        return self.metadata(4)

    def created_date(self):

        """
        If the file is a PDF or DOCX file, try to get a created date out of
        the file metadata.

        Returns:
            datetime|None: The created date.
        """

        ft = self.libmagic_file_type

        if ft == 'application/pdf':
            return utils.pdf_date(self.path)

        else:
            try: return utils.docx_date(self.path)
            except: pass

    @cached_property
    def libmagic_file_type(self):

        """
        Returns:
            str: The libmagic-parsed file type.
        """

        return magic.from_file(self.path, mime=True)

    @property
    @utils.requires_attr('url')
    def domain(self):

        """
        Get the parsed domain of the syllabus' URL.

        Returns:
            str: The top-level domain.
        """

        return parse_domain(self.url())

    @cached_property
    def text(self):

        """
        Extract the raw plain text.

        Returns:
            str: The text content.
        """

        ft = self.libmagic_file_type

        # Empty:
        if ft == 'inode/x-empty':
            return None

        # Plaintext:
        elif ft == 'text/plain':
            with open(self.path, 'r') as fh:
                return fh.read()

        # HTML/XML:
        elif ft == 'text/html':
            return utils.html_text(self.path)

        # PDF:
        elif ft == 'application/pdf':
            return utils.pdf_text(self.path)

        # Everything else:
        else:
            return utils.docx_text(self.path)

    @cached_property
    @utils.requires_attr('text')
    def unbroken_text(self):

        """
        Get rid of linebreaks in the raw text.

        Returns:
            str: The compressed text.
        """

        return re.sub('\s{2,}', ' ', self.text).strip()
