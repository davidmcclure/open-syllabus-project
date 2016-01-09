

import pytest

from osp.common import config
from osp.institutions.models import Institution_Document
from osp.citations.models import Citation_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_index_citation_fields(add_citation):

    """
    Local rows - text_id, document_id, and corpus - should be included in
    the Elasticsearch document.
    """

    citation = add_citation()

    Citation_Index.es_insert()

    doc = config.es.get(
        index='citation',
        id=citation.id,
    )

    assert doc['_source']['text_id'] == citation.text_id
    assert doc['_source']['document_id'] == citation.document_id
    assert doc['_source']['corpus'] == citation.text.corpus


def test_index_field_refs(add_citation, add_subfield, add_subfield_document):

    """
    When the document is linked with a subfield, subfield / field referenecs
    should be included in the document.
    """

    citation = add_citation()
    subfield = add_subfield()

    # Link subfield -> citation.
    add_subfield_document(subfield=subfield, document=citation.document)

    Citation_Index.es_insert()

    doc = config.es.get(
        index='citation',
        id=citation.id,
    )

    assert doc['_source']['subfield_id'] == subfield.id
    assert doc['_source']['field_id'] == subfield.field_id


def test_index_institution_refs(add_citation, add_institution):

    """
    When the document is linked with an institution, an institution reference
    should be included in the document.
    """

    citation = add_citation()

    institution = add_institution(state='CA', country='US')

    # Link inst -> citation.
    Institution_Document.create(
        institution=institution,
        document=citation.document,
    )

    Citation_Index.es_insert()

    doc = config.es.get(
        index='citation',
        id=citation.id,
    )

    assert doc['_source']['institution_id'] == institution.id
    assert doc['_source']['state'] == 'CA'
    assert doc['_source']['country'] == 'US'


def test_only_index_valid_citations(add_citation):

    """
    Only index citations that have been marked as valid.
    """

    c1 = add_citation(valid=None)
    c2 = add_citation(valid=False)
    c3 = add_citation(valid=True)

    Citation_Index.es_insert()

    assert config.es.get(index='citation', id=c3.id)
    assert Citation_Index.es_count() == 1
