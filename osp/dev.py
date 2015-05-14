

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

    docs = (
        Document_Institution
        .select()
        .where(Document_Institution.institution==iid)
    )

    doc_ids = [d._data['document'] for d in docs]

    count = fn.Count(HLOM_Citation.id)

    texts = (

        HLOM_Record
        .select(HLOM_Record, count)

        # Coalesce duplicates.
        .distinct([
            HLOM_Record.metadata['deduping_hash'],
            count
        ])
        .order_by(
            HLOM_Record.metadata['deduping_hash'],
            HLOM_Record.id
        )

        .group_by(HLOM_Record.id)
        .join(HLOM_Citation)
        .where(HLOM_Citation.document << doc_ids)
        .order_by(count.desc())
        .limit(limit)

    )

    for t in texts.naive():
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

    institutions = (
        Institution
        .select()
        .where(Institution.metadata.contains({
            'Institution_State': state
        }))
    )

    inst_ids = [i.id for i in institutions]

    docs = (
        Document_Institution
        .select()
        .where(Document_Institution.institution << inst_ids)
    )

    doc_ids = [d._data['document'] for d in docs]

    count = fn.Count(HLOM_Citation.id)

    texts = (

        HLOM_Record
        .select(HLOM_Record, count)

        # Coalesce duplicates.
        .distinct([
            HLOM_Record.metadata['deduping_hash'],
            count
        ])
        .order_by(
            HLOM_Record.metadata['deduping_hash'],
            HLOM_Record.id
        )

        .group_by(HLOM_Record.id)
        .join(HLOM_Citation)
        .where(HLOM_Citation.document << doc_ids)
        .order_by(count.desc())
        .limit(limit)

    )

    for t in texts.naive():
        print(
            t.count,
            t.pymarc.title(),
            t.pymarc.author()
        )

    # query institutions that match the state
    # hit doc_inst where institution in (ids)
    # get doc_ids, query hlom_record
