

import pytest

from osp.test.corpus.markers import requires_tika
from osp.corpus.syllabus import Syllabus


def test_plaintext(mock_corpus):

    """
    Should extract text from vanilla text files.
    """

    path = mock_corpus.add_file(content='text', ftype='plain')
    syllabus = Syllabus(path)

    assert syllabus.text == 'text'


def test_html(mock_corpus):

    """
    Should extract text from HTML files.
    """

    path = mock_corpus.add_file(content='<p>text</p>', ftype='html')
    syllabus = Syllabus(path)

    assert syllabus.text == 'text'


def test_pdf(mock_corpus):

    """
    Should extract text from PDF files.
    """

    path = mock_corpus.add_file(content='text', ftype='pdf')
    syllabus = Syllabus(path)

    assert syllabus.text.strip() == 'text'


@requires_tika
def test_office(mock_corpus):

    """
    Should extract text from office files.
    """

    path = mock_corpus.add_file(content='text', ftype='docx')
    syllabus = Syllabus(path)

    assert syllabus.text.strip() == 'text'
