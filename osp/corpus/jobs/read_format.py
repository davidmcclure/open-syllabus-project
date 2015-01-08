

from osp.corpus.syllabus import Syllabus
from osp.corpus.models.document_format import DocumentFormat


def read_format(path):

    """
    Write the libmagic file format.

    :param str path: The document path.
    """

    syllabus = Syllabus(path)

    DocumentFormat.create(
        format=syllabus.libmagic_file_type,
        document=syllabus.relative_path
    )
