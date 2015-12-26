

import pytest

from osp.fields.models import Field
from osp.fields.models import Subfield
from osp.fields.models import Subfield_Document
from osp.fields.jobs import doc_to_fields


pytestmark = pytest.mark.usefixtures('db')


def test_matches(add_doc, add_subfield):

    """
    When a document contains a field code, write a doc->field link.
    """

    doc = add_doc(content='abc Field1 101 def Field2 101 ghi')

    sf1 = add_subfield(name='Field1')
    sf2 = add_subfield(name='Field2')
    sf3 = add_subfield(name='Field3')

    doc_to_fields(doc.id)

    # Should write 2 field -> doc links.
    assert Subfield_Document.select().count() == 2

    # Should match the right fields.
    for sf in [sf1, sf2]:

        assert Subfield_Document.select().where(
            Subfield_Document.subfield==sf,
            Subfield_Document.document==doc,
        )


def test_no_matches(add_doc, add_subfield):

    """
    When no fields match, don't write any rows.
    """

    doc = add_doc(content='abc Field2 101 def')

    sf1 = add_subfield(name='Field1')

    doc_to_fields(doc.id)

    # Shouldn't write any rows.
    assert Subfield_Document.select().count() == 0


def test_character_offset(add_doc, add_subfield):

    """
    Record the character offset of the first match.
    """

    #                      01234
    doc = add_doc(content='abc Field1 101 def Field1 201 ghi')

    sf1 = add_subfield(name='Field1')

    doc_to_fields(doc.id)

    assert Subfield_Document.select().where(
        Subfield_Document.subfield==sf1,
        Subfield_Document.document==doc,
        Subfield_Document.offset==3,
    )
