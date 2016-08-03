

import pytest

from osp.common import config

from osp.institutions.models import (
    Institution,
    Institution_Document,
    Institution_Index,
)


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_es_insert(add_institution, add_citation):

    """
    Institution_Index.es_insert() should index institutions with citations.
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

    Institution_Index.es_insert()

    for inst, count in [
        (i1, 3),
        (i2, 2),
        (i3, 1),
    ]:

        doc = config.es.get(
            index='institution',
            id=inst.id,
        )

        assert doc['_source']['name'] == inst.name
        assert doc['_source']['count'] == count
