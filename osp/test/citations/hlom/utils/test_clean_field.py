

from osp.citations.hlom.utils import clean_field


def test_space_on_left():

    """
    clean_field() should strip whitespace from the left of a string.
    """

    assert clean_field('   abc') == 'abc'


def test_space_on_right():

    """
    clean_field() should strip whitespace from the right of a string.
    """

    assert clean_field('abc   ') == 'abc'


def test_punctuation_on_left():

    """
    clean_field() should strip punctuation from the left of a string.
    """

    assert clean_field('.;,abc') == 'abc'


def test_punctuation_on_right():

    """
    clean_field() should strip punctuation from the right of a string.
    """

    assert clean_field('abc.;,') == 'abc'
