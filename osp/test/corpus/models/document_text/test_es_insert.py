

from osp.corpus.models import Document
from osp.corpus.models import Document_Text


def test_es_insert(models, config, corpus_index):

    """
    CorpusIndex.index() should index all rows in Elasticsearch.
    """

    # Index 100 documents.
    for i in range(10):
        doc = Document.create(path=str(i))
        Document_Text.create(document=doc, text=str(i))

    Document_Text.es_insert()

    # Should insert 10 docs.
    assert Document_Text.es_count() == 10

    # For each text row:
    for t in Document_Text.select():

        # A document should exist.
        doc = config.es.get('osp', t.document.id)

        # Should index id + text.
        assert doc['_id'] == str(t.document.id)
        assert doc['_source']['body'] == t.document.path
