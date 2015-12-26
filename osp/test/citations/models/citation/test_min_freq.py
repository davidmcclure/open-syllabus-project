

import pytest

from wordfreq import word_frequency


pytestmark = pytest.mark.usefixtures('db')


def test_min_freq(add_citation):

    """
    Citation#min_freq should provide the scaled word frequency score of the
    most-infrequent match token.
    """

    # one > two > three
    c = add_citation(tokens=['one', 'two', 'three'])

    assert c.min_freq == word_frequency('three', 'en') * 1e6
