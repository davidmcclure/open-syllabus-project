

from osp.citations.models import Citation_Index


def test_docs_with_text(add_text, add_doc, add_citation):

    """
    Citation_Index.docs_with_text() should return a set of ids for documents
    that assign a given text.
    """

    t1 = add_text()
    t2 = add_text()

    d1 = add_doc()
    d2 = add_doc()
    d3 = add_doc()
    d4 = add_doc()

    add_citation(text=t1, document=d1)
    add_citation(text=t1, document=d2)
    add_citation(text=t2, document=d3)
    add_citation(text=t2, document=d4)

    Citation_Index.es_insert()

    doc_ids = Citation_Index.docs_with_text(t1.id)

    assert doc_ids == [d1.id, d2.id]
