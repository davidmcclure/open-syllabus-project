

from osp.corpus.models.document import Document
from osp.corpus.models.text import Document_Text


def text(id):

    """
    Write the document as plain text.

    Args:
        id (int): The document id.
    """

    doc = Document.get(Document.id==id)

    if doc.syllabus.text:

        Document_Text.create(
            text=doc.syllabus.unbroken_text,
            document=doc
        )
