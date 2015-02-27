

from osp.corpus.syllabus import Syllabus


def test_log_path(corpus):

    """
    Syllabys#log_path should return the .log file path.
    """

    path = corpus.add_file()
    syllabus = Syllabus(path)

    assert syllabus.log_path == path+'.log'
