

from peewee import *
from osp.corpus.models.format import Document_Format
from osp.corpus.models.text import Document_Text


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


def document_text(path):

    """
    Get the most recently-extracted text for a document.

    :param path: A corpus-relative document path.
    """

    query = (
        Document_Text
        .select()
        .where(Document_Text.document==path)
        .order_by(Document_Text.created.desc())
    )

    return query.first().text
