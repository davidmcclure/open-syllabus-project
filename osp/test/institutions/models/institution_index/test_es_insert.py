

import pytest

from osp.common import config
from osp.institutions.models import Institution_Index
from osp.institutions.models import Institution


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_es_insert(es, add_institution):

    """
    Institution_Index.es_insert() should index institutions.
    """

    for i in range(10):
        add_institution('inst'+str(i))

    Institution_Index.es_insert()

    for inst in Institution.select():

        doc = config.es.get(
            index='institution',
            id=inst.id,
        )

        assert doc['_source']['name'] == inst.name
