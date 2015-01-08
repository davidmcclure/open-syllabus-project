

from peewee import *
from osp.corpus.models.document_format import Document_Format


def format_counts():

    """
    Map unique file formats to document counts.
    """

    count = fn.Count(Document_Format.id)

    return (
        Document_Format
        .select(Document_Format.format, count.alias('count'))
        .distinct(Document_Format.document)
        .group_by(Document_Format.format)
        .order_by(count.desc())
    )
