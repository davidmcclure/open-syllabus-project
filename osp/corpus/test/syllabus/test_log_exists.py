

import os

from osp.corpus.syllabus import Syllabus


def test_log_exists(mock_corpus):

    """
    Syllabus#log_exists should return True when a log is present.
    """

    path = mock_corpus.add_file()
    syllabus = Syllabus(path)

    assert syllabus.log_exists == True


def test_log_missing(mock_corpus):

    """
    When the log is absent, return False.
    """

    path = mock_corpus.add_file()
    syllabus = Syllabus(path)

    os.remove(path+'.log')
    assert syllabus.log_exists == False
