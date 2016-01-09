

import pytest

from osp.common import config
from osp.fields.models import Subfield
from osp.fields.models import Subfield_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_es_insert():

    """
    Subfield_Index.es_insert() should load all fields into Elasticsearch
    """

    Subfield.ingest()

    Subfield_Index.es_insert()

    for sf in Subfield.select():

        doc = config.es.get(
            index='subfield',
            id=sf.id,
        )

        assert doc['_source']['name'] == sf.name
