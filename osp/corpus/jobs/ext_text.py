

from osp.corpus.models.document import Document
from osp.corpus.models.text import Document_Text


def ext_text(doc_id):

    """
    Write the document as plain text.

    Args:
        doc_id (int): The document id.
    """

    doc = Document.get(Document.id==doc_id)

    if doc.syllabus.text:

        return Document_Text.create(
            text=doc.syllabus.text,
            document=doc
        )
