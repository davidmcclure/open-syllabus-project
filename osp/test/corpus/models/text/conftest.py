

from osp.corpus.models.document import Document
from osp.corpus.models.text import Document_Text


def insert_text(path, text):

    """
    Insert a document / text pair.

    Args:
        path (str): The document path.
        text (str): The fulltext.
    """

    doc = Document.create(path=path)
    return Document_Text.create(document=doc, text=text)


def insert_texts(n, path_prefix='path-', text_prefix='text-'):

    """
    Insert N document / text rows.

    Args:
        n (int): The number of documents.
        path_prefix (str): A prefix for the document paths.
        text_prefix (str): A prefix for the fulltext.
    """

    for i in range(n):
        insert_doc(
            path_prefix+str(i),
            text_prefix+str(i)
        )
