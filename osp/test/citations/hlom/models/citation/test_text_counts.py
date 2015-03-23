

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.jobs.query import query


def test_text_counts(corpus_index, add_hlom, add_doc):

    """
    HLOM_Citation.text_counts() should return a set of (HLOM_Record -> count)
    pairs, sorted in descending order.
    """

    # 1 citation:
    r1 = add_hlom('War and Peace', 'Leo Tolstoy')
    add_doc('War and Peace, Leo Tolstoy')

    # 2 citations:
    r2 = add_hlom('Anna Karenina', 'Leo Tolstoy')
    add_doc('Anna Karenina, Leo Tolstoy b')
    add_doc('Anna Karenina, Leo Tolstoy a')

    # 3 citations:
    r3 = add_hlom('Master and Man', 'Leo Tolstoy')
    add_doc('Master and Man, Leo Tolstoy a')
    add_doc('Master and Man, Leo Tolstoy b')
    add_doc('Master and Man, Leo Tolstoy c')

    corpus_index.index()
    query(r1.id)
    query(r2.id)
    query(r3.id)

    counts = HLOM_Citation.text_counts().naive().iterator()

    c1 = next(counts)
    assert c1.record == r3
    assert c1.count == 3

    c2 = next(counts)
    assert c2.record == r2
    assert c2.count == 2

    c1 = next(counts)
    assert c1.record == r1
    assert c1.count == 1
