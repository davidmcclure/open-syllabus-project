

from osp.corpus.models.document_text import Document_Text
from osp.hlom.models.citation import HLOM_Citation
from osp.hlom.jobs.hlom_to_docs import hlom_to_docs


def test_matches(corpus_index, mock_hlom, add_doc, add_hlom):

    """
    When OSP documents match the query, write link rows.
    """

    d1 = add_doc('War and Peace, Leo Tolstoy 1')
    d2 = add_doc('War and Peace, Leo Tolstoy 2')
    d3 = add_doc('War and Peace, Leo Tolstoy 3')
    d4 = add_doc('Anna Karenina, Leo Tolstoy 1')
    d5 = add_doc('Anna Karenina, Leo Tolstoy 2')

    Document_Text.es_insert()

    record = add_hlom('War and Peace', 'Leo Tolstoy')
    hlom_to_docs(record.id)

    # Should write 3 citation links.
    assert HLOM_Citation.select().count() == 3

    # Should match the right documents.
    for doc in [d1, d2, d3]:

        assert HLOM_Citation.select().where(
            HLOM_Citation.document==doc,
            HLOM_Citation.record==record
        )


def test_no_matches(corpus_index, add_doc, add_hlom):

    """
    When no documents match, don't write any rows.
    """

    add_doc('War and Peace, Leo Tolstoy')
    Document_Text.es_insert()

    record = add_hlom('Master and Man', 'Leo Tolstoy')
    hlom_to_docs(record.id)

    # Shouldn't write any rows.
    assert HLOM_Citation.select().count() == 0
