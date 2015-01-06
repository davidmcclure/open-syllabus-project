

from osp.corpus.syllabus import Syllabus
from osp.corpus.models.format import Format


def read_format(path):

    """
    Write the libmagic file format.

    :param str path: The document path.
    """

    syllabus = Syllabus(path)

    Format.create(
        format=syllabus.libmagic_file_type,
        document=syllabus.relative_path
    )
