

import networkx as nx

from osp.hlom.models.hlom_citation import HLOM_Citation
from osp.hlom.network import Network


def test_add_edges(models, add_hlom, add_doc):

    """
    Network#add_edges() should register edges from the citation table.
    """

    t1 = add_hlom()
    t2 = add_hlom()
    t3 = add_hlom()
    t4 = add_hlom()
    t5 = add_hlom()
    t6 = add_hlom()

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
    n.add_edges()

    assert n.graph.edge[t1.control_number][t2.control_number]['weight'] == 1
    assert n.graph.edge[t2.control_number][t3.control_number]['weight'] == 2
    assert n.graph.edge[t3.control_number][t4.control_number]['weight'] == 3
    assert n.graph.edge[t4.control_number][t5.control_number]['weight'] == 2
    assert n.graph.edge[t5.control_number][t6.control_number]['weight'] == 1


def test_max_citations(models, add_hlom, add_doc):

    """
    Syllabi with more than `max_citations` should be ignored.
    """

    t1 = add_hlom()
    t2 = add_hlom()
    t3 = add_hlom()

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
    n.add_edges(2)

    # Just register citations from s1.
    assert n.graph.edge[t1.control_number][t2.control_number]['weight'] == 1
    assert nx.number_of_edges(n.graph) == 1
