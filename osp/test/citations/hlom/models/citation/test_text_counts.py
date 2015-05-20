

from osp.citations.hlom.models.citation import HLOM_Citation


def test_text_counts(add_hlom, add_doc):

    """
    HLOM_Citation.text_counts() should return a set of (HLOM_Record -> count)
    pairs, sorted in descending order.
    """

    r1 = add_hlom('title1', 'author1')
    r2 = add_hlom('title2', 'author2')
    r3 = add_hlom('title3', 'author3')

    d1 = add_doc('doc1')
    d2 = add_doc('doc2')
    d3 = add_doc('doc3')
    d4 = add_doc('doc4')
    d5 = add_doc('doc5')
    d6 = add_doc('doc6')

    # 1 citation for r1:
    HLOM_Citation.create(record=r1, document=d1)

    # 2 citations for r2:
    HLOM_Citation.create(record=r2, document=d2)
    HLOM_Citation.create(record=r2, document=d3)

    # 3 citations for r3:
    HLOM_Citation.create(record=r3, document=d4)
    HLOM_Citation.create(record=r3, document=d5)
    HLOM_Citation.create(record=r3, document=d6)

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
