

import os

from osp.corpus.syllabus import Syllabus


def test_log_exists(mock_corpus):

    """
    Syllabus#log should split the log file into lines.
    """

    log = {
        'url':          'url',
        'provenance':   'provenance',
        'date':         'date',
        'checksum':     'checksum',
        'format':       'format'
    }

    path = mock_corpus.add_file(log=log)
    syllabus = Syllabus(path)

    assert syllabus.log == [
        'url',
        'provenance',
        'date',
        'checksum',
        'format'
    ]


def test_log_missing(mock_corpus):

    """
    When the log is absent, return an empty list.
    """

    path = mock_corpus.add_file()
    syllabus = Syllabus(path)

    os.remove(path+'.log')
    assert syllabus.log == []
