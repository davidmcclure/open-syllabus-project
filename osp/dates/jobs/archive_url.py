

from osp.corpus.models.document import Document
from osp.dates.models.archive_url import Document_Date_Archive_Url


def archive_url(id):

    """
    Try to extract an Internet Archive timestamp from the URL.

    Args:
        id (int): The document id.
    """

    doc = Document.get(Document.id==id)
    # TODO
