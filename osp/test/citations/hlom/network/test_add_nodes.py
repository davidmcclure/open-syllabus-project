

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.network import Network


def test_build(models, add_hlom, add_doc):

    """
    Network#add_nodes() should register nodes, with title and author.
    """

    # 5 HLOM texts.
    t1 = add_hlom(title='title1', author='author1')
    t2 = add_hlom(title='title2', author='author2')
    t3 = add_hlom(title='title3', author='author3')

    # 1 syllabus.
    s = add_doc('syllabus')

    # Citations for texts 1 and 2.
    HLOM_Citation.create(document=s, record=t1)
    HLOM_Citation.create(document=s, record=t2)

    n = Network()
    n.add_nodes()

    assert n.graph.node[t1.id] == {
        'title': 'title1', 'author': 'author1'
    }
    assert n.graph.node[t2.id] == {
        'title': 'title2', 'author': 'author2'
    }
