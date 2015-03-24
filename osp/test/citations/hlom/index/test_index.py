

from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation


def test_index(models, add_hlom, add_doc, hlom_index):

    """
    CorpusIndex.index() should index cited records in Elasticsearch.
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

    hlom_index.index()

    assert hlom_index.count() == 3
