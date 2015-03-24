

from osp.citations.hlom.utils import sanitize_query


def test_remove_punctuation():

    """
    Punctuation marks should be removed.
    """

    assert sanitize_query('Antonio (Flaminio),') == 'antonio flaminio'


def test_remove_numbers():

    """
    Number should be removed.
    """

    assert sanitize_query('Keats, John, 1795-1821') == 'keats john'
