

import numpy as np

from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation


def test_write_teaching_rank(models, add_hlom, add_doc):

    """
    HLOM_Record.write_teaching_rank() should write 1,2,3... rankings.
    """

    r1 = add_hlom('title1', 'author1')
    r2 = add_hlom('title2', 'author2')
    r3 = add_hlom('title3', 'author3')

    doc = add_doc('content')

    # 1 citation for r1.
    HLOM_Citation.create(record=r1, document=doc)

    # 2 citations for r2.
    HLOM_Citation.create(record=r2, document=doc)
    HLOM_Citation.create(record=r2, document=doc)

    # 3 citations for r3.
    HLOM_Citation.create(record=r3, document=doc)
    HLOM_Citation.create(record=r3, document=doc)
    HLOM_Citation.create(record=r3, document=doc)

    HLOM_Record.write_citation_count()
    HLOM_Record.write_deduping_hash()
    HLOM_Record.write_teaching_rank()

    r1 = HLOM_Record.reload(r1)
    r2 = HLOM_Record.reload(r2)
    r3 = HLOM_Record.reload(r3)

    assert r3.metadata['teaching_rank'] == 1
    assert r2.metadata['teaching_rank'] == 2
    assert r1.metadata['teaching_rank'] == 3

    pct = ((np.log(3)-np.log(2))/np.log(3))*100

    assert r3.metadata['teaching_percent'] == 100
    assert r2.metadata['teaching_percent'] == pct
    assert r1.metadata['teaching_percent'] == 0
