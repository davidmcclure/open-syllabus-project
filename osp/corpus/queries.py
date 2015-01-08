

from peewee import *
from osp.corpus.models.document_format import DocumentFormat


def format_counts():

    """
    Map unique file formats to document counts.
    """

    count = fn.Count(DocumentFormat.id)

    return (
        DocumentFormat
        .select(DocumentFormat.format, count.alias('count'))
        .distinct(DocumentFormat.document)
        .group_by(DocumentFormat.format)
        .order_by(count.desc())
    )
