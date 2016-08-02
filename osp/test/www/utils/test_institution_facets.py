

import pytest

from osp.www.utils import institution_facets
from osp.institutions.models import Institution_Index
from osp.institutions.models import Institution_Document
from osp.citations.models import Citation_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_institution_facets(add_institution, add_citation):

    """
    institution_facets() should provide a list of label/value/count dicts.
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
    Institution_Index.es_insert()

    facets = institution_facets()

    assert facets == [
        dict(label='Institution 1', value=i1.id, count=3),
        dict(label='Institution 2', value=i2.id, count=2),
        dict(label='Institution 3', value=i3.id, count=1),
    ]


def test_include_institutions_outside_of_page(add_institution, add_citation):

    """
    When ids are passed for institutions with counts that fall outside of the
    default page, merge the extra facets onto the bottom of the list.
    """

    i1 = add_institution(name='Institution 1')
    i2 = add_institution(name='Institution 2')
    i3 = add_institution(name='Institution 3')
    i4 = add_institution(name='Institution 3')

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
    Institution_Index.es_insert()

    facets = institution_facets(include=[i3.id, i4.id], depth=2)

    assert facets == [

        dict(label='Institution 1', value=i1.id, count=4),
        dict(label='Institution 2', value=i2.id, count=3),

        # Include 3 and 4.
        dict(label='Institution 3', value=i3.id, count=2),
        dict(label='Institution 4', value=i3.id, count=1),

    ]
