

import pytest

from osp.www.utils import rank_texts
from osp.citations.models import Citation_Index
from osp.citations.models import Text_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_unfiltered(add_text, add_citation):

    """
    When no filters or query is passed, return the overall rankings.
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

    texts = rank_texts()

    assert len(texts['hits']) == 3
    assert texts['hits'][0]['_id'] == str(t1.id)
    assert texts['hits'][1]['_id'] == str(t2.id)
    assert texts['hits'][2]['_id'] == str(t3.id)


def test_metadata_filters(add_text, add_citation):

    """
    Citation metadata filters should be applied.
    """

    t1 = add_text(corpus='corpus1')
    t2 = add_text(corpus='corpus2')
    t3 = add_text(corpus='corpus1')
    t4 = add_text(corpus='corpus2')

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

    texts = rank_texts(filters=dict(
        corpus='corpus2'
    ))

    assert len(texts['hits']) == 2
    assert texts['hits'][0]['_id'] == str(t2.id)
    assert texts['hits'][1]['_id'] == str(t4.id)


def test_search_filter(add_text, add_citation):

    """
    Free-text search query should be applied.
    """

    t1 = add_text(title='match one')
    t2 = add_text(title='two')
    t3 = add_text(title='match three')
    t4 = add_text(title='four')

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

    texts = rank_texts(query='match')

    assert len(texts['hits']) == 2
    assert texts['hits'][0]['_id'] == str(t1.id)
    assert texts['hits'][1]['_id'] == str(t3.id)


def test_size(add_text, add_citation):

    """
    The 'size' argument should control the page length.
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

    texts = rank_texts(size=2)

    assert len(texts['hits']) == 2
    assert texts['hits'][0]['_id'] == str(t1.id)
    assert texts['hits'][1]['_id'] == str(t2.id)


def test_size(add_text, add_citation):

    """
    The 'page' argument should control the page offset.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()
    t4 = add_text()

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

    p1 = rank_texts(size=2, page=1)

    assert len(p1['hits']) == 2
    assert p1['hits'][0]['_id'] == str(t1.id)
    assert p1['hits'][1]['_id'] == str(t2.id)

    p2 = rank_texts(size=2, page=2)

    assert len(p2['hits']) == 2
    assert p2['hits'][0]['_id'] == str(t3.id)
    assert p2['hits'][1]['_id'] == str(t4.id)
