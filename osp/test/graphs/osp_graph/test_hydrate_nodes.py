

import pytest

from osp.graphs.osp_graph import OSP_Graph


pytestmark = pytest.mark.usefixtures('db', 'redis')


def test_hydrate_nodes(add_text, add_doc, add_citation):

    """
    OSP_Graph#hydrate_nodes() should load titles and authors onto nodes.
    """

    t1 = add_text(title='title1', authors=['author1', 'author2'])
    t2 = add_text(title='title2', authors=['author3', 'author4'])

    doc = add_doc()

    add_citation(document=doc, text=t1)
    add_citation(document=doc, text=t2)

    g = OSP_Graph()

    g.add_edges()
    g.hydrate_nodes()

    assert g.graph.node[t1.id]['authors'] == t1.pretty('authors')
    assert g.graph.node[t2.id]['authors'] == t2.pretty('authors')

    assert g.graph.node[t1.id]['title'] == t1.pretty('title')
    assert g.graph.node[t2.id]['title'] == t2.pretty('title')
