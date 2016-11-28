

from osp.corpus.models import Document
from osp.corpus.models import Document_Text


def ext_text(doc_id):

    """
    Write the document as plain text.

    Args:
        doc_id (int): The document id.
    """

    doc = Document.get(Document.id==doc_id)

    text = doc.syllabus.text()

    if text:

        return Document_Text.create(
            text=text,
            document=doc,
        )
