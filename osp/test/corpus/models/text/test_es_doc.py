

from osp.corpus.models.document import Document
from osp.corpus.models.text import Document_Text


def test_es_doc(models):

    """
    Document_Text#es_doc() should return a document for Elasticsearch.
    """

    document = Document.create(path='path')
    text = Document_Text.create(document=document, text='text')

    assert text.es_doc == {
        '_id': 'path',
        'body': 'text'
    }
