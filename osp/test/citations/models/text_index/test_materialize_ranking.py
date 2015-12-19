

import pytest

from osp.citations.models import Citation_Index
from osp.citations.models import Text_Index


@pytest.mark.dev
def test_sort_by_count(add_text, add_citation):

    """
    Results should be sorted by count descending.
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
    Text_Index.es_insert()

    ranks = Citation_Index.rank_texts()
    texts = Text_Index.materialize_ranking(ranks)

    assert texts['hits'][0]['_id'] == str(t3.id)
    assert texts['hits'][1]['_id'] == str(t2.id)
    assert texts['hits'][2]['_id'] == str(t1.id)
