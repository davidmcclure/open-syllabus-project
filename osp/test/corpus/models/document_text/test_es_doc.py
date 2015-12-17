

from osp.corpus.models import Document
from osp.corpus.models import Document_Text


def test_es_doc(models):

    """
    Document_Text#es_doc() should return an Elasticsearch document.
    """

    document = Document.create(path='000/abc')
    text = Document_Text.create(document=document, text='text')

    assert text.es_doc['document_id'] == document.id
    assert text.es_doc['body'] == 'text'
