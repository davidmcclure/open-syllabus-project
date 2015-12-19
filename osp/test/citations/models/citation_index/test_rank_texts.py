

from wordfreq import word_frequency
from osp.citations.models import Citation_Index


def test_unfiltered(add_text, add_citation):

    """
    When no filters are provided, return total counts.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    add_citation(t1)

    add_citation(t2)
    add_citation(t2)

    add_citation(t3)
    add_citation(t3)
    add_citation(t3)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts()

    assert ranks == {
        str(t1.id): 1,
        str(t2.id): 2,
        str(t3.id): 3,
    }


def test_filter_single_value(add_text, add_citation):

    """
    When a single filter value is provided, match citations that include the
    key -> value pair.
    """

    t1 = add_text(corpus='corpus1')
    t2 = add_text(corpus='corpus2')
    t3 = add_text(corpus='corpus2')

    add_citation(t1)

    add_citation(t2)
    add_citation(t2)

    add_citation(t3)
    add_citation(t3)
    add_citation(t3)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts(dict(
        corpus='corpus2'
    ))

    # Just count `corpus2` citations.
    assert ranks == {
        str(t2.id): 2,
        str(t3.id): 3,
    }


def test_filter_multiple_values(add_text, add_citation):

    """
    When a list of values is provided for a filter key, match citations that
    include _any_ of the provided values for the key.
    """

    t1 = add_text(corpus='corpus1')
    t2 = add_text(corpus='corpus2')
    t3 = add_text(corpus='corpus3')

    add_citation(t1)

    add_citation(t2)
    add_citation(t2)

    add_citation(t3)
    add_citation(t3)
    add_citation(t3)

    Citation_Index.es_insert()

    ranks = Citation_Index.rank_texts(dict(
        corpus=['corpus1', 'corpus3']
    ))

    # Count both `corpus1` and `corpus3` citations.
    assert ranks == {
        str(t1.id): 1,
        str(t3.id): 3,
    }


def test_filter_min_freq(add_text, add_citation):

    """
    If a `min_freq` argument is provided, just count citations with a min_freq
    _below_ the passed value.
    """

    text = add_text()

    add_citation(text=text, tokens=['one'])
    add_citation(text=text, tokens=['two'])
    add_citation(text=text, tokens=['three'])
    add_citation(text=text, tokens=['four'])
    add_citation(text=text, tokens=['five'])

    Citation_Index.es_insert()

    for token, count in [
        ('one', 5),
        ('two', 4),
        ('three', 3),
        ('four', 2),
        ('five', 1),
    ]:

        ranks = Citation_Index.rank_texts(
            min_freq=word_frequency(token, 'en')*1e6
        )

        assert ranks == {
            str(text.id): count
        }
