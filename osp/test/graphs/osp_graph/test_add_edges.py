

import pytest

from osp.graphs.osp_graph import OSP_Graph


pytestmark = pytest.mark.usefixtures('db', 'redis')


def test_add_edges(add_text, add_doc, add_citation):

    """
    OSP_Graph#add_edges() should register edges from the citation table.
    """

    d1 = add_doc()
    d2 = add_doc()
    d3 = add_doc()

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()
    t4 = add_text()
    t5 = add_text()
    t6 = add_text()

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

    g = OSP_Graph()

    g.add_edges()

    assert g.graph.edge[t1.id][t2.id]['weight'] == 1
    assert g.graph.edge[t2.id][t3.id]['weight'] == 2
    assert g.graph.edge[t3.id][t4.id]['weight'] == 3
    assert g.graph.edge[t4.id][t5.id]['weight'] == 2
    assert g.graph.edge[t5.id][t6.id]['weight'] == 1


def test_ignore_invalid_texts(add_text, add_doc, add_citation):

    """
    Ignore citations for invalid texts.
    """

    d1 = add_doc()

    t1 = add_text()
    t2 = add_text()
    t3 = add_text(valid=False)

    add_citation(document=d1, text=t1)
    add_citation(document=d1, text=t2)
    add_citation(document=d1, text=t3)

    g = OSP_Graph()

    g.add_edges()

    assert g.graph.has_node(t1.id)
    assert g.graph.has_node(t2.id)

    # Ignore invalid t3.
    assert not g.graph.has_node(t3.id)


def test_ignore_hidden_texts(add_text, add_doc, add_citation):

    """
    Ignore citations for un-displayed texts.
    """

    d1 = add_doc()

    t1 = add_text()
    t2 = add_text()
    t3 = add_text(display=False)

    add_citation(document=d1, text=t1)
    add_citation(document=d1, text=t2)
    add_citation(document=d1, text=t3)

    g = OSP_Graph()

    g.add_edges()

    assert g.graph.has_node(t1.id)
    assert g.graph.has_node(t2.id)

    # Ignore hidden t3.
    assert not g.graph.has_node(t3.id)


def test_ignore_docs_with_too_many_texts(add_text, add_doc, add_citation):

    """
    Ignore docs with more than a given number of texts.
    """

    d1 = add_doc()
    d2 = add_doc()

    t1 = add_text()
    t2 = add_text()

    t3 = add_text()
    t4 = add_text()
    t5 = add_text()

    # 2 citations on d1.
    add_citation(document=d1, text=t1)
    add_citation(document=d1, text=t2)

    # 3 citations on d1.
    add_citation(document=d2, text=t3)
    add_citation(document=d2, text=t4)
    add_citation(document=d2, text=t5)

    g = OSP_Graph()

    g.add_edges(max_texts=2)

    assert g.graph.has_node(t1.id)
    assert g.graph.has_node(t2.id)

    # Ignore texts on d2, which has too many texts.
    assert not g.graph.has_node(t3.id)
    assert not g.graph.has_node(t4.id)
    assert not g.graph.has_node(t5.id)
