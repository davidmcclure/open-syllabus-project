

from osp.corpus.syllabus import Syllabus
from osp.corpus.models.document import Document


def mime_type(path):

    """
    Set the document's mime type.

    :param str path: The document path.
    """

    syllabus = Syllabus(path)

    # Load the document.
    doc = Document.get(Document.path==syllabus.relative_path)

    # Set the mime type.
    doc.metadata['mime_type'] = syllabus.libmagic_file_type
    doc.save()
