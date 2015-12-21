

from osp.web.utils import rank_texts
from osp.citations.models import Citation_Index


def test_filters(add_text, add_citation):

    """
    Citation metadata filters should be applied.
    """

    t1 = add_text(corpus='corpus1')
    t2 = add_text(corpus='corpus2')
    t3 = add_text(corpus='corpus2')

    for i in range(3):
        add_citation(t1)

    for i in range(2):
        add_citation(t2)

    for i in range(1):
        add_citation(t3)

    Citation_Index.es_insert()

    texts = rank_texts(dict(
        corpus='corpus2'
    ))

    assert texts['hits'][0]['_id'] == str(t2.id)
    assert texts['hits'][1]['_id'] == str(t3.id)
