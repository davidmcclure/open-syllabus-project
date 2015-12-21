

from osp.web.utils import field_facets
from osp.citations.models import Citation_Index
from osp.fields.models import Field
from osp.fields.models import Field_Index


def test_subfield_facets(add_citation, add_subfield, add_subfield_document):

    """
    field_facets() should provide a list of label/value/count dicts.
    """

    f1 = Field.create(name='Field 1')
    f2 = Field.create(name='Field 2')
    f3 = Field.create(name='Field 3')

    sf1 = add_subfield(field=f1)
    sf2 = add_subfield(field=f2)
    sf3 = add_subfield(field=f3)

    for i in range(3):
        c = add_citation()
        add_subfield_document(subfield=sf1, document=c.document)

    for i in range(2):
        c = add_citation()
        add_subfield_document(subfield=sf2, document=c.document)

    for i in range(1):
        c = add_citation()
        add_subfield_document(subfield=sf3, document=c.document)

    Citation_Index.es_insert()
    Field_Index.es_insert()

    facets = field_facets()

    assert facets == [
        dict(label='Field 1', value=str(f1.id), count=3),
        dict(label='Field 2', value=str(f2.id), count=2),
        dict(label='Field 3', value=str(f3.id), count=1),
    ]
