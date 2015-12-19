

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


def test_filter_one_corpus(add_text, add_citation):

    """
    When a single corpus value is provided, just count citations for documents
    in that corpus.
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


def test_filter_multiple_corpora(add_text, add_citation):

    """
    When multiple corpus values are provided, count citations for documents in
    any of the provided corpora.
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
