

import pytest

from osp.common.config import config
from osp.citations.models import Text_Index
from osp.citations.models import Text


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_es_insert(add_text, add_citation):

    """
    Text_Index.es_insert() should index texts.
    """

    for i in map(str, range(10)):

        text = add_text(
            corpus      = 'corpus'+i,
            identifier  = 'identifier'+i,
            title       = 'title'+i,
            authors     = ['author1'+i, 'author2'+i],
            publisher   = 'publisher'+i,
            date        = 'date'+i,
            journal     = 'journal'+i,
            url         = 'url'+i,
        )

        # Cite the text.
        add_citation(text=text)

    Text_Index.es_insert()

    for text in Text.select():

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


def test_only_insert_texts_with_valid_citations(add_text, add_citation):

    """
    Skip texts that aren't referenced by valid citations.
    """

    # Valid citation.
    t1 = add_text()
    add_citation(text=t1, valid=True)

    # Invalid citation.
    t2 = add_text()
    add_citation(text=t2, valid=False)

    # Unvalidated citation.
    t3 = add_text()
    add_citation(text=t3, valid=None)

    # No citation.
    t4 = add_text()

    Text_Index.es_insert()

    assert config.es.get(index='text', id=t1.id)
    assert Text_Index.es_count() == 1
