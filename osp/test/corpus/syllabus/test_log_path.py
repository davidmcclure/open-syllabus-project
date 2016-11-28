

from osp.corpus.syllabus import Syllabus


def test_log_path(mock_osp):

    """
    Syllabus#log_path() should return the .log file path.
    """

    path = mock_osp.add_file()
    syllabus = Syllabus(path)

    assert syllabus.log_path() == path+'.log'
