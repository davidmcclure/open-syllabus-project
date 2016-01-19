

import pytest

from osp.graphs.osp_graph import OSP_Graph


pytestmark = pytest.mark.usefixtures('db', 'redis')


def test_add_nodes(add_text, add_citation):

    """
    OSP_Graph#add_nodes() should register nodes for all texts.
    """

    t1 = add_text(title='title1', authors=['author1'])
    t2 = add_text(title='title2', authors=['author2'])

    for i in range(3):
        add_citation(text=t1)

    for i in range(1):
        add_citation(text=t2)

    g = OSP_Graph()

    g.add_nodes()

    n1 = g.graph.node[t1.id]
    n2 = g.graph.node[t2.id]

    assert n1['title'] == t1.pretty('title')
    assert n2['title'] == t2.pretty('title')

    assert n1['authors'] == t1.pretty('authors')[0]
    assert n2['authors'] == t2.pretty('authors')[0]

    assert n1['count'] == 3
    assert n2['count'] == 1

    assert n1['score'] == 2/2
    assert n2['score'] == 1/2
