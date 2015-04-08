

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.network import Network


def test_clear_edges(models, add_hlom, add_doc):

    """
    Network#clear_edges() should remove all edges, but preserve nodes.
    """

    t1 = add_hlom(title='title1', author='author1')
    t2 = add_hlom(title='title2', author='author2')
    s = add_doc('syllabus')

    # 1 co-occurrence of t1 and t2
    HLOM_Citation.create(document=s, record=t1)
    HLOM_Citation.create(document=s, record=t2)

    n = Network()
    n.add_nodes()
    n.add_edges()
    n.clear_edges()

    # Preserve nodes, with data.
    assert n.graph.node[t1.id] == {
        'title': 'title1', 'author': 'author1'
    }
    assert n.graph.node[t2.id] == {
        'title': 'title2', 'author': 'author2'
    }

    # Remove all edges.
    assert n.graph.edge[t1.id] == {}
    assert n.graph.edge[t2.id] == {}
