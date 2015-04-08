

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.network import Network


def test_add_edges(models, add_hlom, add_doc):

    # 5 HLOM texts.
    t1 = add_hlom(title='title1', author='author1')
    t2 = add_hlom(title='title2', author='author2')
    t3 = add_hlom(title='title3', author='author3')
    t4 = add_hlom(title='title4', author='author4')
    t5 = add_hlom(title='title5', author='author5')
    t6 = add_hlom(title='title6', author='author6')

    # 3 syllabi.
    s1 = add_doc('s1')
    s2 = add_doc('s2')
    s3 = add_doc('s3')

    # texts 1-4 in s1.
    HLOM_Citation.create(document=s1, record=t1)
    HLOM_Citation.create(document=s1, record=t2)
    HLOM_Citation.create(document=s1, record=t3)
    HLOM_Citation.create(document=s1, record=t4)

    # texts 2-5 in s2.
    HLOM_Citation.create(document=s2, record=t2)
    HLOM_Citation.create(document=s2, record=t3)
    HLOM_Citation.create(document=s2, record=t4)
    HLOM_Citation.create(document=s2, record=t5)

    # texts 3-6 in s3.
    HLOM_Citation.create(document=s3, record=t3)
    HLOM_Citation.create(document=s3, record=t4)
    HLOM_Citation.create(document=s3, record=t5)
    HLOM_Citation.create(document=s3, record=t6)

    n = Network()
    n.add_nodes()
    n.add_edges()

    assert n.graph.edge[t1.id][t2.id]['weight'] == 1
    assert n.graph.edge[t2.id][t3.id]['weight'] == 2
    assert n.graph.edge[t3.id][t4.id]['weight'] == 3
    assert n.graph.edge[t4.id][t5.id]['weight'] == 2
    assert n.graph.edge[t5.id][t6.id]['weight'] == 1
