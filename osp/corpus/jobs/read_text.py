

from osp.corpus.syllabus import Syllabus
from osp.corpus.models.document_text import Document_Text


def read_text(path):

    """
    Write the document as plaintext.

    :param str path: The document path.
    """

    syllabus = Syllabus(path)

    if syllabus.text:

        Document_Text.create(
            text=syllabus.unbroken_text,
            document=syllabus.relative_path
        )
