

from osp.corpus.syllabus import Syllabus
from osp.corpus.models.file_format import FileFormat


def read_format(path):

    """
    Write the libmagic file format.

    :param str path: The document path.
    """

    syllabus = Syllabus(path)

    FileFormat.create(
        file_format=syllabus.libmagic_file_type,
        document=syllabus.relative_path
    )
