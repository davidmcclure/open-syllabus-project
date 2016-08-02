

import pytest

from osp.citations.models import Citation_Index
from osp.institutions.models import Institution_Document


pytestmark = pytest.mark.usefixtures('db', 'es')


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


def test_include(add_institution, add_citation):

    """
    If an `include` list is passed, just return counts for the passed values.
    """

    i1 = add_institution(name='Institution 1')
    i2 = add_institution(name='Institution 2')
    i3 = add_institution(name='Institution 3')
    i4 = add_institution(name='Institution 4')

    for i in range(4):
        c = add_citation()
        Institution_Document.create(institution=i1, document=c.document)

    for i in range(3):
        c = add_citation()
        Institution_Document.create(institution=i2, document=c.document)

    for i in range(2):
        c = add_citation()
        Institution_Document.create(institution=i3, document=c.document)

    for i in range(1):
        c = add_citation()
        Institution_Document.create(institution=i4, document=c.document)

    Citation_Index.es_insert()

    counts = Citation_Index.count_facets(
        'institution_id',
        include=[i2.id, i4.id],
    )

    # Just include 2 and 4.
    assert counts == [
        (i2.id, 3),
        (i4.id, 1),
    ]
