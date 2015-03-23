

from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation


def test_write_citation_counts(models, add_hlom, add_doc):

    """
    For each record that has at least one citation, write_citation_counts()
    should write the number of citations under a `citation_count` key.
    """

    r1 = add_hlom('title1', 'author1')
    r2 = add_hlom('title2', 'author2')
    r3 = add_hlom('title3', 'author3')

    d1 = add_doc('content1')
    d2 = add_doc('content2')
    d3 = add_doc('content3')

    # 1 citation for r1.
    HLOM_Citation.create(record=r1, document=d1)

    # 2 citations for r2.
    HLOM_Citation.create(record=r2, document=d1)
    HLOM_Citation.create(record=r2, document=d2)

    # 3 citations for r3.
    HLOM_Citation.create(record=r3, document=d1)
    HLOM_Citation.create(record=r3, document=d2)
    HLOM_Citation.create(record=r3, document=d3)

    HLOM_Record.write_citation_counts()

    r1 = HLOM_Record.get(HLOM_Record.id==r1.id)
    r2 = HLOM_Record.get(HLOM_Record.id==r2.id)
    r3 = HLOM_Record.get(HLOM_Record.id==r3.id)

    assert r1.metadata['citation_count'] == 1
    assert r2.metadata['citation_count'] == 2
    assert r3.metadata['citation_count'] == 3
