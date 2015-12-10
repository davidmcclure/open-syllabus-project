

from osp.citations.jobs import text_to_docs
from osp.citations.models import Citation
from osp.corpus.models import Document_Text


def test_matches(corpus_index, add_doc, add_text):

    """
    When OSP documents match the query, write link rows.
    """

    d1 = add_doc(content='War and Peace, Leo Tolstoy 1')
    d2 = add_doc(content='War and Peace, Leo Tolstoy 2')
    d3 = add_doc(content='War and Peace, Leo Tolstoy 3')
    d4 = add_doc(content='Anna Karenina, Leo Tolstoy 1')
    d5 = add_doc(content='Anna Karenina, Leo Tolstoy 2')

    Document_Text.es_insert()

    text = add_text(title='War and Peace', author='Leo Tolstoy')
    text_to_docs(text.id)

    # Should write 3 citation links.
    assert Citation.select().count() == 3

    # Should match the right documents.
    for doc in [d1, d2, d3]:

        assert Citation.select().where(
            Citation.document==doc,
            Citation.text==text
        )


def test_no_matches(corpus_index, add_doc, add_text):

    """
    When no documents match, don't write any rows.
    """

    add_doc(content='War and Peace, Leo Tolstoy')
    Document_Text.es_insert()

    text = add_text(title='Master and Man', author='Leo Tolstoy')
    text_to_docs(text.id)

    # Shouldn't write any rows.
    assert Citation.select().count() == 0
