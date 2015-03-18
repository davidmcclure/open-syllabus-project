

from .conftest import insert_texts
from osp.corpus.models.text import Document_Text


def test_es_index(models, corpus_index, config):

    """
    Document_Text.es_index() should index all rows in Elasticsearch.
    """

    insert_texts(100)

    # Index documents.
    Document_Text.es_index()
    config.es.indices.flush('osp')

    # Should insert 100 docs.
    assert Document_Text.es_count() == 100

    # For each text row:
    for t in Document_Text.select():

        # A document should exist.
        doc = config.es.get('osp', t.document.path)

        # The text should be indexed.
        assert doc['_source']['body'] == t.document.path+' text'
