

def test_es_doc(
    add_citation,
    add_subfield,
    add_subfield_document,
):

    """
    Citation#es_doc should produce a document for Elasticsearch.
    """

    citation = add_citation()

    # Add a subfield.
    subfield = add_subfield()
    add_subfield_document(subfield=subfield, document=citation.document)

    assert citation.es_doc == dict(
        text_id     = citation.text.id,
        document_id = citation.document.id,
        min_freq    = citation.min_freq,
        subfield_id = subfield.id,
        field_id    = subfield.field_id,
    )
