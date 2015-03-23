

from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation


def test_omit_blacklisted(models, add_hlom, add_doc):

    """
    Blacklisted records should be ignored.
    """

    doc = add_doc()

    r1 = add_hlom('title1', 'author1')
    r2 = add_hlom('title2', 'author2')

    HLOM_Citation.create(record=r1, document=doc)
    HLOM_Citation.create(record=r2, document=doc)
    HLOM_Record.write_citation_count()

    # Blacklist r2.
    HLOM_Record.blacklist(r2.control_number)

    query = HLOM_Record.select_cited()
    assert query.count() == 1
    assert query.first().id == r1.id


def test_omit_uncited(models, add_hlom, add_doc):

    """
    Records without citations should be ignored.
    """

    doc = add_doc()

    r1 = add_hlom('title1', 'author1')
    r2 = add_hlom('title2', 'author2')

    # No citation for r2.
    HLOM_Citation.create(record=r1, document=doc)
    HLOM_Record.write_citation_count()

    query = HLOM_Record.select_cited()
    assert query.count() == 1
    assert query.first().id == r1.id


def test_coalesce_duplicates(models, add_hlom, add_doc):

    """
    Duplicate records should be combined.
    """

    doc = add_doc()

    r1 = add_hlom('title1', 'author1')
    r2 = add_hlom('title1', 'author1')

    r3 = add_hlom('title2', 'author2')
    r4 = add_hlom('title2', 'author2')

    r5 = add_hlom('title3', 'author3')
    r6 = add_hlom('title3', 'author3')

    HLOM_Citation.create(record=r1, document=doc)
    HLOM_Citation.create(record=r2, document=doc)
    HLOM_Citation.create(record=r3, document=doc)
    HLOM_Citation.create(record=r4, document=doc)
    HLOM_Citation.create(record=r5, document=doc)
    HLOM_Citation.create(record=r6, document=doc)
    HLOM_Record.write_citation_count()

    HLOM_Record.write_deduping_hash()

    query = HLOM_Record.select_cited()
    ids = [r.id for r in query]

    assert len(ids) == 3
    assert r1.id in ids
    assert r3.id in ids
    assert r5.id in ids
