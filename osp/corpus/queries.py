

from peewee import *
from osp.corpus.models.file_format import FileFormat


def format_counts():

    """
    Map unique file formats to document counts.
    """

    count = fn.Count(FileFormat.id)

    return (
        FileFormat
        .select(FileFormat.file_format, count.alias('count'))
        .distinct(FileFormat.document)
        .group_by(FileFormat.file_format)
        .order_by(count.desc())
    )
