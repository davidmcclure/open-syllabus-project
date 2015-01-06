

from peewee import *
from osp.corpus.models.format import Format


def format_counts():

    """
    Map unique file formats to document counts.
    """

    count = fn.Count(Format.id)

    return (
        Format
        .select(Format.format, count.alias('count'))
        .distinct(Format.document)
        .group_by(Format.format)
        .order_by(count.desc())
    )
