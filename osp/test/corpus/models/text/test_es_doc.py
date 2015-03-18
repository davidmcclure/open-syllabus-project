

from .conftest import insert_text


def test_es_doc(models):

    """
    Document_Text#es_doc() should return a document for Elasticsearch.
    """

    text = insert_text('000/abc')

    assert text.es_doc == {
        '_id': '000/abc',
        'body': '000/abc text'
    }
