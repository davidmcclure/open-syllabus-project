

def test_es_doc(add_citation):

    """
    Citation#es_doc should produce a document for Elasticsearch.
    """

    citation = add_citation()

    assert citation.es_doc == dict(
        text_id     = citation.text.id,
        document_id = citation.document.id,
        min_freq    = citation.min_freq,
    )
