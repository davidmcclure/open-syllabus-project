

from osp.corpus.models import Document
from osp.corpus.models import Document_Text


def test_es_doc(models):

    """
    Document_Text#es_doc() should return an Elasticsearch document.
    """

    doc = Document.create(path='000/abc')
    text = Document_Text.create(document=doc, text='text')

    assert text.es_doc['_id'] == '000/abc'
    assert text.es_doc['document_id'] == doc.id
    assert text.es_doc['body'] == 'text'
