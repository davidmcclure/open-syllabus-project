

from osp.common.config import config

from osp.fields.models import Subfield
from osp.fields.models import Subfield_Index


def test_es_insert(es):

    """
    Subfield_Index.es_insert() should load all fields into Elasticsearch
    """

    Subfield.ingest()

    Subfield_Index.es_insert()

    for sf in Subfield.select():

        doc = config.es.get(
            index='osp',
            doc_type='subfield',
            id=sf.id,
        )

        assert doc['_source']['name'] == sf.name
