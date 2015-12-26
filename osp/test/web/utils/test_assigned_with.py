

import pytest

from osp.web.utils import assigned_with
from osp.citations.models import Citation_Index
from osp.citations.models import Text_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_assigned_with(add_text, add_doc, add_citation):

    """
    Given a seed text, assigned_with() should pull a ranking for all texts that
    are co-assigned on a syllabus with the seed.
    """

    t1 = add_text(corpus='hlom', identifier='001')

    t2 = add_text()
    t3 = add_text()
    t4 = add_text()

    for i in range(3):
        doc = add_doc()
        add_citation(text=t1, document=doc)
        add_citation(text=t2, document=doc)

    for i in range(2):
        doc = add_doc()
        add_citation(text=t1, document=doc)
        add_citation(text=t3, document=doc)

    for i in range(1):
        doc = add_doc()
        add_citation(text=t1, document=doc)
        add_citation(text=t4, document=doc)

    Citation_Index.es_insert()
    Text_Index.es_insert()

    texts = assigned_with('hlom', '001')

    assert len(texts['hits']) == 3
    assert texts['hits'][0]['_id'] == str(t2.id)
    assert texts['hits'][1]['_id'] == str(t3.id)
    assert texts['hits'][2]['_id'] == str(t4.id)
