

from osp.corpus.models.document import Document


def insert(path):

    """
    Insert a canonical record for a document.

    :param path: The corpus-relative path.
    """

    Document.create(path=path)
