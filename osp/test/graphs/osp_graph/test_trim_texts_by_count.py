

import pytest

from osp.graphs.osp_graph import OSP_Graph


pytestmark = pytest.mark.usefixtures('db', 'redis')


def test_trim_texts_by_count(add_text, add_doc, add_citation):

    """
    OSP_Graph#trim_texts_by_count() should remove all texts with fewer than a
    given number of total citations.
    """

    docs = [
        add_doc(),
        add_doc(),
        add_doc(),
        add_doc(),
    ]

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()
    t4 = add_text()

    # 4 citations to t1.
    for i in range(4):
        add_citation(document=docs[i], text=t1)

    # 3 citations to t2.
    for i in range(3):
        add_citation(document=docs[i], text=t2)

    # 2 citations to t3.
    for i in range(2):
        add_citation(document=docs[i], text=t3)

    # 1 citation to t4.
    for i in range(1):
        add_citation(document=docs[i], text=t4)

    g = OSP_Graph()

    g.add_edges()
    g.add_nodes()

    g.trim_texts_by_count(min_count=3)

    assert g.graph.has_node(t1.id)
    assert g.graph.has_node(t2.id)

    assert not g.graph.has_node(t3.id)
    assert not g.graph.has_node(t4.id)
