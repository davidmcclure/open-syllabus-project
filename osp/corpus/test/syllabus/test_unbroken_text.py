

import os

from osp.corpus.syllabus import Syllabus


def test_collapse_whitespace(corpus):

    """
    Should collapse all 2-char+ strings of whitespace.
    """

    text = 'w1 \n\t w2 \n\t w3'

    path = corpus.add_file(content=text, ftype='plain')
    syllabus = Syllabus(path)

    assert syllabus.unbroken_text == 'w1 w2 w3'


def test_trim(corpus):

    """
    Should trim whitespace from the beginnging and end.
    """

    text = ' \n\t word \n\t '

    path = corpus.add_file(content=text, ftype='plain')
    syllabus = Syllabus(path)

    assert syllabus.unbroken_text == 'word'
