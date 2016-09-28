

from osp.corpus.models import Document
from osp.corpus.models import Document_Format


def ext_format(doc_id):

    """
    Write the libmagic file format.

    Args:
        doc_id (int): The document id.
    """

    doc = Document.get(Document.id==doc_id)

    syllabus = doc.syllabus()

    return Document_Format.create(
        format=syllabus.libmagic_file_type,
        document=doc,
    )
