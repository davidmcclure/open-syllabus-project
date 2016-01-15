

import pytest

from osp.graphs.text_graph import Text_Graph


pytestmark = pytest.mark.usefixtures('db', 'redis')


def test_add_edges(add_text, add_doc, add_citation):

    """
    Text_Graph#add_edges() should register edges from the citation table.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()
    t4 = add_text()
    t5 = add_text()
    t6 = add_text()

    d1 = add_doc()
    d2 = add_doc()
    d3 = add_doc()

    # Texts 1-4 in d1.
    add_citation(document=d1, text=t1)
    add_citation(document=d1, text=t2)
    add_citation(document=d1, text=t3)
    add_citation(document=d1, text=t4)

    # Texts 2-5 in d2.
    add_citation(document=d2, text=t2)
    add_citation(document=d2, text=t3)
    add_citation(document=d2, text=t4)
    add_citation(document=d2, text=t5)

    # Texts 3-6 in d3.
    add_citation(document=d3, text=t3)
    add_citation(document=d3, text=t4)
    add_citation(document=d3, text=t5)
    add_citation(document=d3, text=t6)

    g = Text_Graph()

    g.add_edges()

    assert g.graph.edge[t1.id][t2.id]['weight'] == 1
    assert g.graph.edge[t2.id][t3.id]['weight'] == 2
    assert g.graph.edge[t3.id][t4.id]['weight'] == 3
    assert g.graph.edge[t4.id][t5.id]['weight'] == 2
    assert g.graph.edge[t5.id][t6.id]['weight'] == 1
