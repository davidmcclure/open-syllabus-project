

from osp.common.config import config

from osp.institutions.models import Institution
from osp.institutions.models import Institution_Index


def test_es_insert(es, add_institution):

    """
    Institution_Index.es_insert() should index institutions.
    """

    for i in range(10):
        add_institution('inst'+str(i))

    Institution_Index.es_insert()

    for inst in Institution.select():

        doc = config.es.get(
            index='osp',
            doc_type='institution',
            id=inst.id,
        )

        assert doc['_source']['name'] == inst.name
