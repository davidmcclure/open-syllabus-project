

import pytest


def test_hash(add_text):

    """
    Text#hash should generate a unique hash for a text.
    """

    t1 = add_text(title='Anna Karenina', author='Leo Tolstoy')
    t2 = add_text(title='ANNA KARENINA', author='LEO TOLSTOY')
    t3 = add_text(title='War and Peace', author='Leo Tolstoy')

    assert t1.hash == t2.hash != t3.hash
