

from osp.corpus.models import Document
from osp.corpus.models import Document_Text


def ext_text(doc_id):

    """
    Write the document as plain text.

    Args:
        doc_id (int): The document id.
    """

    doc = Document.get(Document.id==doc_id)

    syllabus = doc.syllabus()

    if syllabus.text:

        return Document_Text.create(
            text=syllabus.text,
            document=doc,
        )
