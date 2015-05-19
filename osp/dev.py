

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.models.record import HLOM_Record
from osp.locations.models.doc_inst import Document_Institution
from osp.institutions.models.institution import Institution
from peewee import fn


def institution_ranks(iid, limit=500):

    """
    Get text rankings for an institution.

    Args:
        iid (int): The institution id.
    """

    count = fn.Count(HLOM_Citation.id)

    texts = (

        HLOM_Record
        .select(HLOM_Record, count)
        .group_by(HLOM_Record.id)

        # Coalesce duplicates.
        .distinct([
            HLOM_Record.metadata['deduping_hash'],
            count
        ])
        .order_by(
            HLOM_Record.metadata['deduping_hash'],
            HLOM_Record.id
        )

        .join(HLOM_Citation)
        .join(Document_Institution, on=(
            HLOM_Citation.document==Document_Institution.document
        ))

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

        HLOM_Record
        .select(HLOM_Record, count)
        .group_by(HLOM_Record.id)

        # Coalesce duplicates.
        .distinct([
            HLOM_Record.metadata['deduping_hash'],
            count
        ])
        .order_by(
            HLOM_Record.metadata['deduping_hash'],
            HLOM_Record.id
        )

        .join(HLOM_Citation)
        .join(Document_Institution, on=(
            HLOM_Citation.document==Document_Institution.document
        ))
        .join(Institution)

        .where(Institution.metadata['Institution_State']==state)

        .order_by(count.desc())

    )

    for t in texts.limit(limit).naive():
        print(
            t.count,
            t.pymarc.title(),
            t.pymarc.author()
        )
