

import pytest

from osp.graphs.osp_graph import OSP_Graph


pytestmark = pytest.mark.usefixtures('db', 'redis')


def test_add_nodes(add_text, add_citation):

    """
    OSP_Graph#add_nodes() should register nodes for all texts.
    """

    t1 = add_text(title='title1', surname='surname1')
    t2 = add_text(title='title2', surname='surname2')

    for i in range(3):
        add_citation(text=t1)

    for i in range(1):
        add_citation(text=t2)

    g = OSP_Graph()

    g.add_nodes()

    n1 = g.graph.node[t1.id]
    n2 = g.graph.node[t2.id]

    assert n1['label'] == t1.pretty('title')
    assert n2['label'] == t2.pretty('title')

    assert n1['author'] == t1.pretty('surname')
    assert n2['author'] == t2.pretty('surname')

    assert n1['count'] == 3
    assert n2['count'] == 1

    assert n1['score'] == 2/2
    assert n2['score'] == 1/2
