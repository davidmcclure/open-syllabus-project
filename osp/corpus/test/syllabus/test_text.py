

import os

from osp.corpus.syllabus import Syllabus


def test_plaintext(corpus):

    """
    Should extract text from vanilla text files.
    """

    path = corpus.add_file(ftype='plain', content='text')
    syllabus = Syllabus(path)

    assert syllabus.text == 'text'
