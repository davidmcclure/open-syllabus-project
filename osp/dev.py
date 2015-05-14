

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.models.record import HLOM_Record
from osp.locations.models.doc_inst import Document_Institution
from peewee import fn


def ranks(iid, limit=500):

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
        .group_by(HLOM_Record.id)
        .order_by(
            HLOM_Record.metadata['deduping_hash'],
            HLOM_Record.id
        )

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
