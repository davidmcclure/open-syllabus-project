

from osp.corpus.models.document import Document
from osp.corpus.models.text import Document_Text


def insert_text(path):

    """
    Insert a document / text pair.

    Args:
        path (str): The document path.

    Returns:
        Document_Text
    """

    doc = Document.create(path=path)

    return Document_Text.create(
        document=doc,
        text=path+' text'
    )


def insert_texts(n, path_prefix='path-'):

    """
    Insert N document / text rows.

    Args:
        n (int): The number of documents.
        path_prefix (str): A prefix for the document paths.
        text_prefix (str): A prefix for the fulltext.
    """

    for i in range(n):
        insert_text(path_prefix+str(i))
