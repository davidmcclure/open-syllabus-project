

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.models.record_cited import HLOM_Record_Cited
from osp.locations.models.doc_inst import Document_Institution
from osp.institutions.models.institution import Institution
from peewee import fn


def all_ranks(limit=500):

    """
    Get unfiltered rankings.
    """

    count = fn.Count(HLOM_Citation.id)

    texts = (

        HLOM_Record_Cited
        .select(HLOM_Record_Cited, count)

        # Join citations.
        .join(HLOM_Citation, on=(
            HLOM_Record_Cited.id==HLOM_Citation.record
        ))

        .group_by(HLOM_Record_Cited.id)
        .order_by(count.desc())

    )

    for t in texts.limit(limit).naive():
        print(
            t.count,
            t.pymarc.title(),
            t.pymarc.author()
        )


def institution_ranks(iid, limit=500):

    """
    Get text rankings for an institution.

    Args:
        iid (int): The institution id.
    """

    count = fn.Count(HLOM_Citation.id)

    texts = (

        HLOM_Record_Cited
        .select(HLOM_Record_Cited, count)
        .group_by(HLOM_Record_Cited.id)

        # Join citations.
        .join(HLOM_Citation, on=(
            HLOM_Record_Cited.id==HLOM_Citation.record
        ))

        # Join institutions.
        .join(Document_Institution, on=(
            HLOM_Citation.document==Document_Institution.document
        ))

        # Filter by institution.
        .where(Document_Institution.institution==iid)
        .order_by(count.desc())

    )

    for t in texts.limit(limit).naive():
        print(
            t.count,
            t.pymarc.title(),
            t.pymarc.author()
        )


def state_ranks(state, limit=500):

    """
    Get text rankings for a state.

    Args:
        state (str): The state abbreviation.
    """

    count = fn.Count(HLOM_Citation.id)

    texts = (

        HLOM_Record_Cited
        .select(HLOM_Record_Cited, count)
        .group_by(HLOM_Record_Cited.id)

        # Join citations.
        .join(HLOM_Citation, on=(
            HLOM_Record_Cited.id==HLOM_Citation.record
        ))

        # Filter by state.
        .where(HLOM_Citation.state==state)
        .order_by(count.desc())

    )

    for t in texts.limit(limit).naive():
        print(
            t.count,
            t.pymarc.title(),
            t.pymarc.author()
        )
