

import os

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
