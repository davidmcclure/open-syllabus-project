

import pytest


pytestmark = pytest.mark.usefixtures('db')


def test_subfield(
    add_doc,
    add_subfield,
    add_subfield_document,
    add_citation
):

    """
    Citation#subfield should provide the document's subfield.
    """

    document = add_doc()

    sf1 = add_subfield()
    sf2 = add_subfield()
    sf3 = add_subfield()

    # Link subfields -> document.
    add_subfield_document(subfield=sf1, document=document, offset=1)
    add_subfield_document(subfield=sf2, document=document, offset=2)
    add_subfield_document(subfield=sf3, document=document, offset=3)

    citation = add_citation(document=document)

    # Return subfield with first offset.
    assert citation.subfield.id == sf1.id


def test_no_subfield(add_citation):

    """
    When no institution is linked, return None.
    """

    citation = add_citation()

    assert citation.subfield == None
