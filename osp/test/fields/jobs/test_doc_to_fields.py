

from osp.corpus.models import Document_Text
from osp.fields.models import Field
from osp.fields.models import Field_Document
from osp.fields.jobs.doc_to_fields import doc_to_fields


def test_matches(models, add_doc):

    """
    When a document contains a field code, write a doc->field link.
    """

    doc = add_doc(content='abc Field1 101 def Field2 101 ghi')

    f1 = Field.create(secondary_field='Field1')
    f2 = Field.create(secondary_field='Field2')
    f3 = Field.create(secondary_field='Field3')

    doc_to_fields(doc.id)

    # Should write 2 citation links.
    assert Field_Document.select().count() == 2

    # Should match the right fields.
    for field in [f1, f2]:

        assert Field_Document.select().where(
            Field_Document.field==field,
            Field_Document.document==doc,
        )


def test_no_matches(models, add_doc):

    """
    When no fields match, don't write any rows.
    """

    doc = add_doc(content='abc Field2 101 def')

    f1 = Field.create(secondary_field='Field1')

    doc_to_fields(doc.id)

    # Shouldn't write any rows.
    assert Field_Document.select().count() == 0
