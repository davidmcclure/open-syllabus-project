

import os

from osp.corpus.syllabus import Syllabus


def test_collapse_whitespace(mock_osp):

    """
    Should collapse all 2-char+ strings of whitespace.
    """

    text = 'w1 \n\t w2 \n\t w3'

    path = mock_osp.add_file(content=text, ftype='plain')
    syllabus = Syllabus(path)

    assert syllabus.unbroken_text() == 'w1 w2 w3'


def test_trim(mock_osp):

    """
    Should trim whitespace from the beginnging and end.
    """

    text = ' \n\t word \n\t '

    path = mock_osp.add_file(content=text, ftype='plain')
    syllabus = Syllabus(path)

    assert syllabus.unbroken_text() == 'word'
