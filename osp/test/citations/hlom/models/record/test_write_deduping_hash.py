

from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation


def test_write_deduping_hash(models, add_hlom, add_doc):

    """
    HLOM_Record.write_deduping_hash() should write deduping hashes into the
    `metadata` columns for each record that has at least 1 citation.
    """

    r1 = add_hlom('title1', 'author1')
    r2 = add_hlom('title2', 'author2')
    r3 = add_hlom('title3', 'author3')
    r4 = add_hlom('title4', 'author4')

    d1 = add_doc('content1')
    d2 = add_doc('content2')
    d3 = add_doc('content3')

    HLOM_Citation.create(record=r1, document=d1)
    HLOM_Citation.create(record=r2, document=d2)
    HLOM_Citation.create(record=r3, document=d3)

    HLOM_Record.write_deduping_hash()

    assert (
        HLOM_Record
        .select()
        .where(HLOM_Record.metadata.contains('deduping_hash'))
    ).count() == 3

