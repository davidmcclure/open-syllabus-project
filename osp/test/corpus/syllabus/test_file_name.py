

from osp.corpus.syllabus import Syllabus


def test_file_name(mock_osp):

    """
    Syllabus#file_name Should return the base file name.
    """

    path = mock_osp.add_file(name='name')
    syllabus = Syllabus(path)

    assert syllabus.file_name() == 'name'
