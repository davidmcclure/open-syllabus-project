

import pytest

from osp.citations.models import Citation_Index
from osp.citations.models import Text_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_sort_on_total_counts_by_default(add_text, add_citation):

    """
    By default return results sorted on the total citation count.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    for i in range(3):
        add_citation(text=t1)

    for i in range(2):
        add_citation(text=t2)

    for i in range(1):
        add_citation(text=t3)

    Text_Index.es_insert()

    texts = Text_Index.materialize_ranking()

    assert texts['hits'][0]['_id'] == str(t1.id)
    assert texts['hits'][1]['_id'] == str(t2.id)
    assert texts['hits'][2]['_id'] == str(t3.id)


def test_sort_on_filtered_counts(add_text, add_citation):

    """
    If a text -> count map is passed, sort on the filtered counts.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    for i in range(30):
        add_citation(text=t1)

    for i in range(20):
        add_citation(text=t2)

    for i in range(10):
        add_citation(text=t3)

    Text_Index.es_insert()

    texts = Text_Index.materialize_ranking(ranks={
        t1.id: 1,
        t2.id: 2,
        t3.id: 3,
    })

    assert texts['hits'][0]['_id'] == str(t3.id)
    assert texts['hits'][1]['_id'] == str(t2.id)
    assert texts['hits'][2]['_id'] == str(t1.id)


@pytest.mark.parametrize('params', [
    lambda x: dict(title=x),
    lambda x: dict(authors=[x]),
    lambda x: dict(publisher=x),
    lambda x: dict(journal_title=x),
])
def test_search_on_total_counts(params, add_text, add_citation):

    """
    If a search query is provided, filter the results on the query.
    """

    t1 = add_text(**params('match one'))
    t2 = add_text(**params('two'))
    t3 = add_text(**params('match three'))
    t4 = add_text(**params('four'))

    for i in range(4):
        add_citation(text=t1)

    for i in range(3):
        add_citation(text=t2)

    for i in range(2):
        add_citation(text=t3)

    for i in range(1):
        add_citation(text=t4)

    Text_Index.es_insert()

    texts = Text_Index.materialize_ranking(query='match')

    assert len(texts['hits']) == 2
    assert texts['hits'][0]['_id'] == str(t1.id)
    assert texts['hits'][1]['_id'] == str(t3.id)


def test_paginate_results(add_text, add_citation):

    """
    When a page is provided, return the 1-indexed page.
    """

    # 9 texts - the first with 9 citations, second with 8, etc.

    texts = []
    for i in reversed(range(1, 10)):

        text = add_text()

        for j in range(i):
            add_citation(text=text)

        texts.append(text)

    Text_Index.es_insert()

    # Get first page by default.
    p1 = Text_Index.materialize_ranking(size=3)

    assert len(p1['hits']) == 3
    assert p1['hits'][0]['_id'] == str(texts[0].id)
    assert p1['hits'][1]['_id'] == str(texts[1].id)
    assert p1['hits'][2]['_id'] == str(texts[2].id)

    p2 = Text_Index.materialize_ranking(size=3, page=2)

    assert len(p1['hits']) == 3
    assert p2['hits'][0]['_id'] == str(texts[3].id)
    assert p2['hits'][1]['_id'] == str(texts[4].id)
    assert p2['hits'][2]['_id'] == str(texts[5].id)

    p3 = Text_Index.materialize_ranking(size=3, page=3)

    assert len(p1['hits']) == 3
    assert p3['hits'][0]['_id'] == str(texts[6].id)
    assert p3['hits'][1]['_id'] == str(texts[7].id)
    assert p3['hits'][2]['_id'] == str(texts[8].id)
