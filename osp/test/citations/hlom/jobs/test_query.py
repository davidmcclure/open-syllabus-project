

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.jobs.query import query


def test_matches(corpus_index, mock_hlom, doc, hlom):

    """
    When OSP documents match the query, write link rows.
    """

    d1 = doc('War and Peace, Leo Tolstoy 1')
    d2 = doc('War and Peace, Leo Tolstoy 2')
    d3 = doc('War and Peace, Leo Tolstoy 3')
    d4 = doc('Anna Karenina, Leo Tolstoy 1')
    d5 = doc('Anna Karenina, Leo Tolstoy 2')

    corpus_index.index()

    record = hlom('War and Peace', 'Leo Tolstoy')
    query(record.id)

    # Should write 3 citation links.
    assert HLOM_Citation.select().count() == 3

    # Should match the right documents.
    for doc in [d1, d2, d3]:

        assert HLOM_Citation.select().where(
            HLOM_Citation.document==doc,
            HLOM_Citation.record==record
        )


def test_no_matches(corpus_index, doc, hlom):

    """
    When no documents match, don't write any rows.
    """

    doc('War and Peace, Leo Tolstoy')
    corpus_index.index()

    record = hlom('Master and Man', 'Leo Tolstoy')
    query(record.id)

    # Shouldn't write any rows.
    assert HLOM_Citation.select().count() == 0
