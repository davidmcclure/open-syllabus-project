

from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation


def test_omit_blacklisted(models, add_hlom, add_doc):

    """
    Blacklisted records should be ignored.
    """

    r1 = add_hlom('title1', 'author1')
    r2 = add_hlom('title2', 'author2')

    d1 = add_doc('content1')
    d2 = add_doc('content2')

    HLOM_Citation.create(record=r1, document=d1)
    HLOM_Citation.create(record=r2, document=d2)
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

    r1 = add_hlom('title1', 'author1')
    r2 = add_hlom('title2', 'author2')

    d1 = add_doc('content1')
    d2 = add_doc('content2')

    # No citation for r2.
    HLOM_Citation.create(record=r1, document=d1)
    HLOM_Record.write_citation_count()

    query = HLOM_Record.select_cited()
    assert query.count() == 1
    assert query.first().id == r1.id


def test_coalesce_duplicates():

    """
    Duplicate records should be combined.
    """

    pass
