

import os
import tldextract
import re

from contextlib import contextmanager
from functools import lru_cache
from osp.corpus.utils import requires_attr


class Syllabus:


    def __init__(self, path):

        """
        Initialize the syllabus reader.

        :param path: The syllabus path.
        """

        self.path = os.path.abspath(path)


    @contextmanager
    def open(self):

        """
        Get an open file handler to the syllabus.
        """

        with open(self.path, 'r') as syllabus:
            yield syllabus


    @property
    def file_name(self):

        """
        Get the file name of the document.
        """

        return os.path.basename(self.path)


    @property
    def segment_name(self):

        """
        Get the name of the parent segment.
        """

        return os.path.split(os.path.dirname(self.path))[-1]


    @property
    def relative_path(self):

        """
        Get the file path relative to the corpus.
        """

        return self.segment_name+'/'+self.file_name


    @property
    def log_path(self):

        """
        Get the path to the corresponding log file.
        """

        return self.path+'.log'


    @property
    @lru_cache()
    def log(self):

        """
        Get the log file as an array of elements.
        """

        with open(self.log_path, 'r') as log:
            try: return log.read().splitlines()
            except: return False


    def metadata(self, offset):

        """
        Get a manifest element, identified by offset.

        :param offset: The 0-indexed offset.
        """

        try: return self.log[offset]
        except: return None


    @property
    def url(self):

        """
        The URL the syllabus was scraped from.
        """

        return self.metadata(0)


    @property
    def provenance(self):

        """
        The origin of the file.
        """

        return self.metadata(1)


    @property
    def retrieved(self):

        """
        The date the file was scraped.
        """

        return self.metadata(2)


    @property
    def checksum(self):

        """
        The checksum for the file.
        """

        return self.metadata(3)


    @property
    def mime_type(self):

        """
        The mime type of the file.
        """

        return self.metadata(4)


    @property
    @requires_attr('url')
    def parsed_domain(self):

        """
        Get the parsed domain of the syllabus' URL.

        @returns: tldextract `ExtractResult`.
        """

        # Get the last `http://` group.
        http = re.compile('http[s]?:/{1,2}')
        last = http.split(self.url)[-1]

        return tldextract.extract(last)


    @property
    @requires_attr('url')
    def registered_domain(self):

        """
        Get the registered domain of the syllabus' URL. Eg:
        http://www.yale.edu/syllabus.pdf -> yale.edu

        @returns: The registered domain.
        """

        return self.parsed_domain.registered_domain
