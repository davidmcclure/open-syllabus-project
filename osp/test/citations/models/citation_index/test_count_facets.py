

from osp.citations.models import Citation_Index


def test_count_facets(add_citation, add_subfield, add_subfield_document):

    """
    Citation_Index.count_facets() should return a set of (value, count) tuples
    for a given field.
    """

    sf1 = add_subfield()
    sf2 = add_subfield()
    sf3 = add_subfield()

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

    counts = Citation_Index.count_facets('subfield_id')

    assert counts == [
        (sf1.id, 3),
        (sf2.id, 2),
        (sf3.id, 1),
    ]
