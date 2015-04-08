

import networkx as nx

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.network import Network


def test_add_edges(models, add_hlom, add_doc):

    """
    Network#add_edges() should register edges from the citation table.
    """

    t1 = add_hlom(title='title1', author='author1')
    t2 = add_hlom(title='title2', author='author2')
    t3 = add_hlom(title='title3', author='author3')
    t4 = add_hlom(title='title4', author='author4')
    t5 = add_hlom(title='title5', author='author5')
    t6 = add_hlom(title='title6', author='author6')

    s1 = add_doc('syllabus1')
    s2 = add_doc('syllabus2')
    s3 = add_doc('syllabus3')

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


def test_clear_existing_edges(models, add_hlom, add_doc):

    """
    When add_edges() is called, existing edges in the network should be
    cleared before the list is rebuilt.
    """

    t1 = add_hlom(title='title1', author='author2')
    t2 = add_hlom(title='title2', author='author2')
    s = add_doc('syllabus')

    # 1 co-occurrence of t1 and t2
    HLOM_Citation.create(document=s, record=t1)
    HLOM_Citation.create(document=s, record=t2)

    n = Network()
    n.add_nodes()

    # Add edges twice.
    n.add_edges()
    n.add_edges()

    assert n.graph.edge[t1.id][t2.id]['weight'] == 1


def test_max_citations(models, add_hlom, add_doc):

    """
    Syllabi with more than `max_citations` should be ignored.
    """

    t1 = add_hlom(title='title1', author='author1')
    t2 = add_hlom(title='title2', author='author2')
    t3 = add_hlom(title='title3', author='author3')

    s1 = add_doc('syllabus1')
    s2 = add_doc('syllabus2')

    # 2 citations in s1.
    HLOM_Citation.create(document=s1, record=t1)
    HLOM_Citation.create(document=s1, record=t2)

    # 3 citations in s2.
    HLOM_Citation.create(document=s2, record=t1)
    HLOM_Citation.create(document=s2, record=t2)
    HLOM_Citation.create(document=s2, record=t3)

    n = Network()
    n.add_nodes()
    n.add_edges(2)

    # Just register citations from s1.
    assert n.graph.edge[t1.id][t2.id]['weight'] == 1
    assert nx.number_of_edges(n.graph) == 1
