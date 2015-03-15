

from osp.corpus.models.document import Document
from osp.corpus.models.format import Document_Format


def ext_format(doc_id):

    """
    Write the libmagic file format.

    Args:
        doc_id (int): The document id.
    """

    doc = Document.get(Document.id==doc_id)

    return Document_Format.create(
        format=doc.syllabus.libmagic_file_type,
        document=doc
    )
