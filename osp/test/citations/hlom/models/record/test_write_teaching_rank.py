

from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation


def test_write_teaching_rank(models, add_hlom, add_doc):

    """
    HLOM_Record.write_teaching_rank() should write 1,2,3... rankings.
    """

    r1 = add_hlom('title1', 'author1')
    r2 = add_hlom('title2', 'author2')
    r3 = add_hlom('title3', 'author3')
    r4 = add_hlom('title4', 'author4')

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

    HLOM_Record.write_teaching_rank()

    r1 = HLOM_Record.reload(r1)
    r2 = HLOM_Record.reload(r2)
    r3 = HLOM_Record.reload(r3)
    r4 = HLOM_Record.reload(r4)

    assert r1.metadata['teaching_rank'] == 3
    assert r2.metadata['teaching_rank'] == 2
    assert r3.metadata['teaching_rank'] == 1

    # No rank on r4.
    assert 'teaching_rank' not in r4.metadata
