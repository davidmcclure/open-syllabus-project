

from osp.institutions.models import Institution_Document


def test_citation_fields(add_citation):

    """
    Local rows - text_id, document_id, and min_freq - should be included in
    the Elasticsearch document.
    """

    citation = add_citation()

    doc = citation.es_doc

    assert doc['citation_id'] == citation.id
    assert doc['text_id'] == citation.text_id
    assert doc['document_id'] == citation.document_id
    assert doc['corpus'] == citation.text.corpus
    assert doc['min_freq'] == citation.min_freq


def test_field_refs(add_citation, add_subfield, add_subfield_document):

    """
    When the document is linked with a subfield, subfield / field referenecs
    should be included in the document.
    """

    citation = add_citation()
    subfield = add_subfield()

    # Link subfield -> citation.
    add_subfield_document(subfield=subfield, document=citation.document)

    doc = citation.es_doc

    assert doc['subfield_id'] == subfield.id
    assert doc['field_id'] == subfield.field_id


def test_institution_refs(add_citation, add_institution):

    """
    When the document is linked with an institution, an institution reference
    should be included in the document.
    """

    citation = add_citation()

    institution = add_institution()

    # Link inst -> citation.
    Institution_Document.create(
        institution=institution,
        document=citation.document,
    )

    doc = citation.es_doc

    assert doc['institution_id'] == institution.id
