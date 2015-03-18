

from .conftest import insert_text


def test_es_doc(models):

    """
    Document_Text#es_doc() should return a document for Elasticsearch.
    """

    text = insert_text('path', 'text')

    assert text.es_doc == {
        '_id': 'path',
        'body': 'text'
    }
