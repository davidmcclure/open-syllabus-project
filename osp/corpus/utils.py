

import os
import subprocess
import requests
import re

from osp.common.config import config
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader
from docx import Document
from nltk.stem import PorterStemmer
from datetime import datetime


def requires_attr(attr):

    """
    If the instance doesn't have an attribute, return None.

    Args:
        attr (str): The required attribute.

    Returns:
        function: The decorated function.
    """

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if getattr(self, attr, None):
                return func(self, *args, **kwargs)
            else: return None
        return wrapper
    return decorator


def int_to_dir(i):

    """
    Convert an integer offset to a segment name.

    Args:
        i (int): The integer offset.

    Returns:
        str: The segment directory name.
    """

    return hex(i)[2:].zfill(3)


def html_text(path, exclude=['script', 'style']):

    """
    Convert HTML to text.

    Args:
        path (str): The file path.
        exclude (list): A list of tags to ignore.

    Returns:
        str: The extracted text.
    """

    with open(path, 'rb') as fh:

        soup = BeautifulSoup(fh)
        for script in soup(exclude): script.extract()
        return soup.get_text()


def pdf_text(path):

    """
    Convert a PDF to text.

    Args:
        path (str): The file path.

    Returns:
        str: The extracted text.
    """

    cmd = os.path.join(config['osp']['bin'], 'pdf2txt.py')
    txt = subprocess.check_output([cmd, path])
    return txt.decode('utf8')


def docx_text(path):

    """
    Convert to plaintext with LibreOffice.

    Args:
        path (str): The file path.

    Returns:
        str: The extracted text.
    """

    with open(path, 'rb') as fh:

        r = requests.put(
            config['tika']['server'],
            headers={'Accept': 'text/plain'},
            data=fh.read()
        )

        return r.text


def pdf_date(path):

    """
    Extract a date from PDF file metadata.

    Args:
        path (str): The file path.

    Returns:
        datetime: The created date.
    """

    reader = PdfFileReader(path)

    # Get rid of `D:` prefix and timezone.
    stamp = reader.documentInfo['/CreationDate']
    match = re.search('\d+', stamp)

    return datetime.strptime(
        match.group(),
        '%Y%m%d%H%M%S'
    )


def docx_date(path):

    """
    Extract a date from DOCX file metadata.

    Args:
        path (str): The file path.

    Returns:
        datetime: The created date.
    """

    return Document(path).core_properties.created


def tokenize(text):

    """
    Yield tokens.

    Args:
        text (str): The original text.

    Yields:
        dict: The next token.
    """

    stem = PorterStemmer().stem
    tokens = re.finditer('[a-z]+', text.lower())

    for offset, match in enumerate(tokens):

        # Get the raw token.
        unstemmed = match.group(0)

        yield { # Emit the token.
            'stemmed':      stem(unstemmed),
            'unstemmed':    unstemmed,
            'offset':       offset
        }
