

from osp.corpus.models.text import Document_Text
from osp.fields.models.field import Field
from osp.fields.models.field_document import Field_Document
from osp.fields.jobs.query import query


def test_match_secondary_fields(add_doc):

    """
    Field queries should match secondary field names + numbers.
    """

    d1 = add_doc('History 101')
    d2 = add_doc('History 201')
    d3 = add_doc('English 101')

    Document_Text.es_insert()

    history = Field.create(secondary_field='History')
    query(history.id)

    assert Field_Document.select().count() == 2
