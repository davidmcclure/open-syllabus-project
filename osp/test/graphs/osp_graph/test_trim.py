

import pytest

from osp.graphs.osp_graph import OSP_Graph


pytestmark = pytest.mark.usefixtures('db', 'redis')


def test_trim(add_text, add_doc, add_citation):

    """
    OSP_Graph#trim() should remove all but the largest component.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    t4 = add_text()
    t5 = add_text()

    d1 = add_doc()
    d2 = add_doc()

    # 3-node component.
    add_citation(document=d1, text=t1)
    add_citation(document=d1, text=t2)
    add_citation(document=d1, text=t3)

    # 2-node component.
    add_citation(document=d2, text=t4)
    add_citation(document=d2, text=t5)

    g = OSP_Graph()

    g.add_edges()

    g.trim()

    # Keep largest component.
    assert g.graph.has_node(t1.id)
    assert g.graph.has_node(t2.id)
    assert g.graph.has_node(t3.id)

    # Remove smaller component.
    assert not g.graph.has_node(t4.id)
    assert not g.graph.has_node(t5.id)
