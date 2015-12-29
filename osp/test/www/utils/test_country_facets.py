

import pytest

from osp.www.utils import country_facets
from osp.institutions.models import Institution_Index
from osp.institutions.models import Institution_Document
from osp.citations.models import Citation_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_country_facets(add_institution, add_citation):

    """
    country_facets() should provide a list of label/value/count dicts.
    """

    i1 = add_institution(country='AU')
    i2 = add_institution(country='CA')
    i3 = add_institution(country='NZ')

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

    facets = country_facets()

    assert facets == [
        dict(label='Australia', value=i1.country, count=3),
        dict(label='Canada', value=i2.country, count=2),
        dict(label='New Zealand', value=i3.country, count=1),
    ]
