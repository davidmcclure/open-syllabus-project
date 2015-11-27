

from osp.hlom.utils import prettify_field


def test_space_on_left():

    """
    Strip whitespace from the left of a string.
    """

    assert prettify_field('   abc') == 'abc'


def test_space_on_right():

    """
    Strip whitespace from the right of a string.
    """

    assert prettify_field('abc   ') == 'abc'


def test_punctuation_on_left():

    """
    Strip punctuation from the left of a string.
    """

    assert prettify_field('.;,abc') == 'abc'


def test_punctuation_on_right():

    """
    Strip punctuation from the right of a string.
    """

    assert prettify_field('abc.;,') == 'abc'


def test_keep_parens():

    """
    Leave in parentheses, which are often legitimate.
    """

    assert prettify_field('(abc) def') == '(abc) def'
    assert prettify_field('abc (def)') == 'abc (def)'
