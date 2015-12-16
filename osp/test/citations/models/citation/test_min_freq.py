

from wordfreq import word_frequency


def test_min_freq(add_citation):

    # one > two > three
    c = add_citation(tokens=['one', 'two', 'three'])

    assert c.min_freq == word_frequency('three', 'en') * 1e6
