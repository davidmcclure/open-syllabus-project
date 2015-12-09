

from osp.corpus.models import Document_Text
from osp.citations.models import Citation
from osp.citations.jobs import hlom_to_docs


def test_matches(corpus_index, mock_hlom, add_doc, add_hlom):

    """
    When OSP documents match the query, write link rows.
    """

    d1 = add_doc(content='War and Peace, Leo Tolstoy 1')
    d2 = add_doc(content='War and Peace, Leo Tolstoy 2')
    d3 = add_doc(content='War and Peace, Leo Tolstoy 3')
    d4 = add_doc(content='Anna Karenina, Leo Tolstoy 1')
    d5 = add_doc(content='Anna Karenina, Leo Tolstoy 2')

    Document_Text.es_insert()

    record = add_hlom(title='War and Peace', author='Leo Tolstoy')
    hlom_to_docs(record.id)

    # Should write 3 citation links.
    assert Citation.select().count() == 3

    # Should match the right documents.
    for doc in [d1, d2, d3]:

        assert Citation.select().where(
            Citation.document==doc,
            Citation.record==record
        )


def test_no_matches(corpus_index, add_doc, add_hlom):

    """
    When no documents match, don't write any rows.
    """

    add_doc(content='War and Peace, Leo Tolstoy')
    Document_Text.es_insert()

    record = add_hlom(title='Master and Man', author='Leo Tolstoy')
    hlom_to_docs(record.id)

    # Shouldn't write any rows.
    assert Citation.select().count() == 0
