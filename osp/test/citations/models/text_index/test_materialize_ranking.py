

import pytest

from osp.citations.models import Citation_Index
from osp.citations.models import Text_Index


def test_sort_by_count(add_text, add_citation):

    """
    Results should be sorted by count descending.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    for i in range(3):
        add_citation(t1)

    for i in range(2):
        add_citation(t2)

    for i in range(1):
        add_citation(t3)

    Citation_Index.es_insert()
    Text_Index.es_insert()

    ranks = Citation_Index.rank_texts()
    texts = Text_Index.materialize_ranking(ranks)

    assert texts['hits'][0]['_id'] == str(t1.id)
    assert texts['hits'][1]['_id'] == str(t2.id)
    assert texts['hits'][2]['_id'] == str(t3.id)


def test_query_title(add_text, add_citation):

    """
    If a search query is passed, filter results on title.
    """

    t1 = add_text(title='David McClure')
    t2 = add_text(title='Joe Karaganis')
    t3 = add_text(title='David William')
    t4 = add_text(title='Dennis Tenen')

    for i in range(4):
        add_citation(t1)

    for i in range(3):
        add_citation(t2)

    for i in range(2):
        add_citation(t3)

    for i in range(1):
        add_citation(t4)

    Citation_Index.es_insert()
    Text_Index.es_insert()

    ranks = Citation_Index.rank_texts()
    texts = Text_Index.materialize_ranking(ranks, query='David')

    assert len(texts['hits']) == 2
    assert texts['hits'][0]['_id'] == str(t1.id)
    assert texts['hits'][1]['_id'] == str(t3.id)
