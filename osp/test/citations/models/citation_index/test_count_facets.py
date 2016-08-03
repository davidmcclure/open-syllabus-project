

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


def test_append_included_facets(add_institution, add_citation):

    """
    When "included" facets have counts that put them below of the baseline
    ranking, append the extra facets to the bottom of the list.
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
        include=[i3.id, i4.id],
        depth=2,
    )

    assert counts == [

        (i1.id, 4),
        (i2.id, 3),

        # Include 3 and 4.
        (i3.id, 2),
        (i4.id, 1),

    ]


def test_merge_included_facets(add_institution, add_citation):

    """
    Don't duplicate included facets are already present in the ranking.
    """

    i1 = add_institution(name='Institution 1')
    i2 = add_institution(name='Institution 2')
    i3 = add_institution(name='Institution 3')

    for i in range(3):
        c = add_citation()
        Institution_Document.create(institution=i1, document=c.document)

    for i in range(2):
        c = add_citation()
        Institution_Document.create(institution=i2, document=c.document)

    for i in range(1):
        c = add_citation()
        Institution_Document.create(institution=i3, document=c.document)

    Citation_Index.es_insert()

    counts = Citation_Index.count_facets(
        'institution_id',
        include=[i2.id, i3.id],
    )

    # Dedupe 2 and 3.
    assert counts == [
        (i1.id, 3),
        (i2.id, 2),
        (i3.id, 1),
    ]
