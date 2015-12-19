

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
