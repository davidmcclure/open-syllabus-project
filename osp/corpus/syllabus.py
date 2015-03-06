

import os
import tldextract
import re
import magic
import re

import osp.corpus.utils as utils
from osp.common.config import config
from contextlib import contextmanager
from functools import lru_cache


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

        print(config.config)
        path = os.path.join(config['osp']['corpus'], relative_path)
        return cls(path)


    def __init__(self, path):

        """
        Initialize a syllabus reader.

        Args:
            path (str): The file path.
        """

        self.path = os.path.abspath(path)


    @property
    def file_name(self):

        """
        Returns:
            str: The file name of the document.
        """

        return os.path.basename(self.path)


    @property
    def segment_name(self):

        """
        Returns:
            str: The name of the parent segment.
        """

        return os.path.split(os.path.dirname(self.path))[-1]


    @property
    def relative_path(self):

        """
        Returns:
            str: The file path, relative to the corpus.
        """

        return self.segment_name+'/'+self.file_name


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


    @property
    @lru_cache()
    def log(self):

        """
        Get the log file as an array of elements.

        Returns:
            list: Log elements.
        """

        if self.log_exists:
            with open(self.log_path, 'r') as log:
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


    @property
    def url(self):

        """
        Returns:
            str: The URL the file was scraped from.
        """

        return self.metadata(0)


    @property
    def provenance(self):

        """
        Returns:
            str: The origin of the file.
        """

        return self.metadata(1)


    @property
    def date(self):

        """
        Returns:
            str: The date the file was scraped.
        """

        return self.metadata(2)


    @property
    def checksum(self):

        """
        Returns:
            str: The checksum for the file.
        """

        return self.metadata(3)


    @property
    def file_type(self):

        """
        Returns:
            str: The mime type of the file.
        """

        return self.metadata(4)


    @property
    @lru_cache()
    def libmagic_file_type(self):

        """
        Returns:
            str: The libmagic-parsed file type.
        """

        return magic.from_file(self.path, mime=True).decode('utf-8')


    @property
    @utils.requires_attr('url')
    def parsed_domain(self):

        """
        Get the parsed domain of the syllabus' URL.

        Returns:
            str: The top-level domain.
        """

        # Get the last `http://` group.
        http = re.compile('http[s]?:/{1,2}')
        last = http.split(self.url)[-1]

        return tldextract.extract(last)


    @property
    @utils.requires_attr('url')
    def registered_domain(self):

        """
        Get the registered domain of the syllabus' URL. Eg:
        http://www.yale.edu/syllabus.pdf -> yale.edu

        Returns:
            str: The base URL.
        """

        return self.parsed_domain.registered_domain


    @property
    @lru_cache()
    def text(self):

        """
        Extract the raw plain text.

        Returns:
            str: The text content.
        """

        ft = self.libmagic_file_type
        text = None

        # Plaintext:
        if ft == 'text/plain':
            with open(self.path, 'r') as fh:
                return fh.read()

        # HTML/XML:
        elif ft == 'text/html':
            return utils.html_to_text(self.path)

        # PDF:
        elif ft == 'application/pdf':
            return utils.pdf_to_text(self.path)

        # Everything else:
        else:
            return utils.office_to_text(self.path)


    @property
    @lru_cache()
    @utils.requires_attr('text')
    def unbroken_text(self):

        """
        Get rid of linebreaks in the raw text.

        Returns:
            str: The compressed text.
        """

        return re.sub('\s{2,}', ' ', self.text).strip()
