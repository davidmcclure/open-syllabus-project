

from osp.corpus.models import Document_Text
from osp.fields.models import Subfield
from osp.fields.models import Subfield_Document
from osp.fields.jobs import doc_to_fields


def test_matches(models, add_doc):

    """
    When a document contains a field code, write a doc->field link.
    """

    doc = add_doc(content='abc Field1 101 def Field2 101 ghi')

    sf1 = Subfield.create(name='Field1')
    sf2 = Subfield.create(name='Field2')
    sf3 = Subfield.create(name='Field3')

    doc_to_fields(doc.id)

    # Should write 2 citation links.
    assert Subfield_Document.select().count() == 2

    # Should match the right fields.
    for subfield in [sf1, sf2]:

        assert Subfield_Document.select().where(
            Subfield_Document.subfield==subfield,
            Subfield_Document.document==doc,
        )


def test_no_matches(models, add_doc):

    """
    When no fields match, don't write any rows.
    """

    doc = add_doc(content='abc Field2 101 def')

    sf1 = Subfield.create(name='Field1')

    doc_to_fields(doc.id)

    # Shouldn't write any rows.
    assert Subfield_Document.select().count() == 0
