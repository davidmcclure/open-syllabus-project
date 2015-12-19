

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
