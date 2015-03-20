

from .conftest import insert_texts
from osp.corpus.models.text import Document_Text


def test_index(models, corpus_index, config):

    """
    Document_Text.es_index() should index all rows in Elasticsearch.
    """

    # Index documents.
    insert_texts(100)
    corpus_index.index()

    # Should insert 100 docs.
    assert corpus_index.count() == 100

    # For each text row:
    for t in Document_Text.select():

        # A document should exist.
        doc = corpus_index.es.get('osp', t.document.path)

        # Should index text / doc ID.
        assert doc['_source']['doc_id'] == t.document.id
        assert doc['_source']['body']   == t.document.path
