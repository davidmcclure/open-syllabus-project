

import os

from osp.corpus.syllabus import Syllabus


def test_log_exists(corpus):

    """
    Syllabys#log_exists should return True when a log is present.
    """

    path = corpus.add_file()
    syllabus = Syllabus(path)

    assert syllabus.log_exists == True


def test_log_missing(corpus):

    """
    When the log is absent, return False.
    """

    path = corpus.add_file()
    syllabus = Syllabus(path)

    os.remove(path+'.log')
    assert syllabus.log_exists == False
