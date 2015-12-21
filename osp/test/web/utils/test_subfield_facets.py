

from osp.web.utils import subfield_facets
from osp.citations.models import Citation_Index
from osp.fields.models import Subfield_Index


def test_subfield_facets(add_citation, add_subfield, add_subfield_document):

    """
    subfield_facets() should provide a list of label/value/count dicts.
    """

    sf1 = add_subfield(name='Subfield 1')
    sf2 = add_subfield(name='Subfield 2')
    sf3 = add_subfield(name='Subfield 3')

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
    Subfield_Index.es_insert()

    facets = subfield_facets()

    assert facets == [
        dict(label='Subfield 1', value=str(sf1.id), count=3),
        dict(label='Subfield 2', value=str(sf2.id), count=2),
        dict(label='Subfield 3', value=str(sf3.id), count=1),
    ]
