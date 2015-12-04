

from osp.corpus.models.text import Document_Text
from osp.fields.models.field import Field
from osp.fields.models.field_document import Field_Document
from osp.fields.jobs.ext_fields import ext_fields


def test_matches(models, add_doc):

    """
    When a document contains a field code, write a doc->field link.
    """

    doc = add_doc('abc Field1 101 def Field2 101 ghi')

    f1 = Field.create(secondary_field='Field1')
    f2 = Field.create(secondary_field='Field2')
    f3 = Field.create(secondary_field='Field3')

    Document_Text.es_insert()
    ext_fields(doc.id)

    # Should write 2 citation links.
    assert Field_Document.select().count() == 2

    # Should match the right fields.
    for field in [f1, f2]:

        assert Field_Document.select().where(
            Field_Document.field==field,
            Field_Document.document==doc,
        )
