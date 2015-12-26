

import pytest

from osp.common.config import config
from osp.fields.models import Subfield
from osp.fields.models import Field
from osp.fields.models import Field_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_es_insert():

    """
    Field_Index.es_insert() should load all fields into Elasticsearch
    """

    Subfield.ingest()

    Field_Index.es_insert()

    for field in Field.select():

        doc = config.es.get(
            index='osp',
            doc_type='field',
            id=field.id,
        )

        assert doc['_source']['name'] == field.name
