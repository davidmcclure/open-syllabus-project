

import os
import tldextract
import re
import PyPDF2
import magic

import osp.corpus.utils as utils
from contextlib import contextmanager
from functools import lru_cache


class Syllabus:


    def __init__(self, path):

        """
        Initialize a syllabus reader.

        :param path: The syllabus path.
        """

        self.path = os.path.abspath(path)


    @contextmanager
    def open(self):

        """
        Get an open file handler to the syllabus.
        """

        with open(self.path, 'rb') as syllabus:
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
    def file_type(self):

        """
        The mime type of the file.
        """

        return self.metadata(4)


    @property
    @lru_cache()
    def libmagic_file_type(self):

        """
        Parse the file type with libmagic.
        """

        return magic.from_file(self.path, mime=True).decode('utf-8')


    @property
    @utils.requires_attr('url')
    def parsed_domain(self):

        """
        Get the parsed domain of the syllabus' URL.
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
        """

        return self.parsed_domain.registered_domain


    @property
    @lru_cache()
    def text(self):

        """
        Extract the raw plain text.
        """

        ft = self.libmagic_file_type

        with self.open() as f:

            if ft == 'text/plain':
                return f.read()

            elif ft in ['text/html', 'application/xml']:
                return utils.html_to_text(f.read())

            elif ft == 'application/pdf':
                return utils.pdf_to_text(f)


    @property
    @lru_cache()
    def unbroken_text(self):

        """
        Get rid of linebreaks in the raw text.
        """

        lines = [line for line in self.text.splitlines() if line]
        return ' '.join(lines)
