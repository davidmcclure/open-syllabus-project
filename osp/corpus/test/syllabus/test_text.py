

import pytest

from osp.corpus.test.markers import requires_tika
from osp.corpus.syllabus import Syllabus


def test_plaintext(corpus):

    """
    Should extract text from vanilla text files.
    """

    path = corpus.add_file(content='text', ftype='plain')
    syllabus = Syllabus(path)

    assert syllabus.text == 'text'


def test_html(corpus):

    """
    Should extract text from HTML files.
    """

    path = corpus.add_file(content='<p>text</p>', ftype='html')
    syllabus = Syllabus(path)

    assert syllabus.text == 'text'


def test_pdf(corpus):

    """
    Should extract text from PDF files.
    """

    path = corpus.add_file(content='text', ftype='pdf')
    syllabus = Syllabus(path)

    assert syllabus.text.strip() == 'text'


@requires_tika
def test_office(corpus):

    """
    Should extract text from office files.
    """

    path = corpus.add_file(content='text', ftype='docx')
    syllabus = Syllabus(path)

    assert syllabus.text.strip() == 'text'
