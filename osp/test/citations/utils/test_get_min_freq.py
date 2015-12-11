

from wordfreq import word_frequency

from osp.citations.utils import get_min_freq


def test_get_min_freq():

    """
    get_min_freq() should return the frequency score of the most infrequent
    token in the passed list.
    """

    mf = get_min_freq(['the', 'a', 'cat'])

    assert mf == word_frequency('cat', 'en')
