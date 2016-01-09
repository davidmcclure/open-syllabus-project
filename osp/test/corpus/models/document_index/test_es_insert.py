

import pytest

from osp.common import config
from osp.corpus.models import Document_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_es_insert(add_doc):

    """
    Document_Index.es_insert() should index the document body and id.
    """

    doc = add_doc(content='text')

    Document_Index.es_insert()

    es_doc = config.es.get(
        index='document',
        id=doc.id,
    )

    assert es_doc['_source']['body'] == 'text'
