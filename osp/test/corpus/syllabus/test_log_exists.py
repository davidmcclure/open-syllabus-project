

import os

from osp.corpus.syllabus import Syllabus


def test_log_exists(mock_osp):

    """
    Syllabus#log_exists() should return True when a log is present.
    """

    path = mock_osp.add_file()
    syllabus = Syllabus(path)

    assert syllabus.log_exists() == True


def test_log_missing(mock_osp):

    """
    When the log is absent, return False.
    """

    path = mock_osp.add_file()
    syllabus = Syllabus(path)

    os.remove(path+'.log')
    assert syllabus.log_exists() == False
