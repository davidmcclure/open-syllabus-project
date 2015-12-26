

import pytest

from osp.web.utils import state_facets
from osp.institutions.models import Institution_Index
from osp.institutions.models import Institution_Document
from osp.citations.models import Citation_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_state_facets(add_institution, add_citation):

    """
    state_facets() should provide a list of label/value/count dicts.
    """

    i1 = add_institution(state='CA')
    i2 = add_institution(state='AL')
    i3 = add_institution(state='MA')

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

    facets = state_facets()

    assert facets == [
        dict(label='California', value=i1.state, count=3),
        dict(label='Alabama', value=i2.state, count=2),
        dict(label='Massachusetts', value=i3.state, count=1),
    ]
