

import pytest

from osp.common import config
from osp.citations.models import Text_Index
from osp.citations.models import Text


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_index_metadata(add_text, add_citation):

    """
    Text_Index.es_insert() should index texts.
    """

    text = add_text(
        corpus      = 'corpus',
        identifier  = 'identifier',
        title       = 'title',
        authors     = ['author1', 'author2'],
        publisher   = 'publisher',
        date        = 'date',
        journal     = 'journal',
        url         = 'url',
    )

    # Cite the text.
    add_citation(text=text)

    Text_Index.es_insert()

    doc = config.es.get(
        index='text',
        id=text.id,
    )

    assert doc['_source']['corpus']     == text.corpus
    assert doc['_source']['identifier'] == text.identifier
    assert doc['_source']['title']      == text.pretty('title')
    assert doc['_source']['authors']    == text.pretty('authors')
    assert doc['_source']['publisher']  == text.pretty('publisher')
    assert doc['_source']['date']       == text.pretty('date')
    assert doc['_source']['journal']    == text.pretty('journal_title')
    assert doc['_source']['url']        == text.url


def test_index_counts_and_ranks(add_text, add_citation):

    """
    Index total citation counts and ranks.
    """

    t1 = add_text()
    t2 = add_text()

    t3 = add_text()
    t4 = add_text()

    t5 = add_text()
    t6 = add_text()

    for i in range(3):
        add_citation(text=t1)
        add_citation(text=t2)

    for i in range(2):
        add_citation(text=t3)
        add_citation(text=t4)

    for i in range(1):
        add_citation(text=t5)
        add_citation(text=t6)

    Text_Index.es_insert()

    for t in [t1, t2]:
        doc = config.es.get(index='text', id=t.id)
        assert doc['_source']['rank'] == 1
        assert doc['_source']['count'] == 3

    for t in [t3, t4]:
        doc = config.es.get(index='text', id=t.id)
        assert doc['_source']['rank'] == 3
        assert doc['_source']['count'] == 2

    for t in [t5, t6]:
        doc = config.es.get(index='text', id=t.id)
        assert doc['_source']['rank'] == 5
        assert doc['_source']['count'] == 1
