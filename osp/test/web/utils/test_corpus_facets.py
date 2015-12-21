

from osp.web.utils import corpus_facets
from osp.citations.models import Citation_Index


def test_corpus_facets(add_text, add_citation):

    """
    corpus_facets() should provide a list of label/value/count dicts.
    """

    t1 = add_text(corpus='hlom')
    t2 = add_text(corpus='jstor')

    for i in range(2):
        c = add_citation(text=t1)

    for i in range(1):
        c = add_citation(text=t2)

    Citation_Index.es_insert()

    facets = corpus_facets()

    assert facets == [
        dict(label='Harvard Library Open Metadata', value='hlom', count=2),
        dict(label='JSTOR', value='jstor', count=1),
    ]
