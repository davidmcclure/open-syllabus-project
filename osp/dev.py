

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.locations.models.doc_inst import Document_Institution
from peewee import fn


def rank(iid):

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
        HLOM_Citation
        .select(HLOM_Citation.record, count.alias('count'))
        .where(HLOM_Citation.document << doc_ids)
        .group_by(HLOM_Citation.record)
        .distinct(HLOM_Citation.record)
        .order_by(count.desc())
        .limit(100)
    )

    for t in texts.naive():
        print(t.count, t.record.pymarc.title())
