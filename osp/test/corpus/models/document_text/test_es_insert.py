

from osp.common.config import config
from osp.corpus.models import Document
from osp.corpus.models import Document_Text


def test_es_insert(corpus_index, add_doc):

    """
    Document_Text.es_insert() should index the document body and id.
    """

    doc = add_doc(content='text')

    Document_Text.es_insert()

    es_doc = config.es.get(
        index='osp',
        doc_type='document',
        id=doc.id,
    )

    assert es_doc['_id'] == str(doc.id)
    assert es_doc['_source']['body'] == 'text'
