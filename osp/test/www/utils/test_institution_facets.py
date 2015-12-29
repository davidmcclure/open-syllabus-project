

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
        dict(label='Institution 1', value=str(i1.id), count=3),
        dict(label='Institution 2', value=str(i2.id), count=2),
        dict(label='Institution 3', value=str(i3.id), count=1),
    ]
