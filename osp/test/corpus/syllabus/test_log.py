

import os

from osp.corpus.syllabus import Syllabus


def test_log_exists(mock_osp):

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

    path = mock_osp.add_file(log=log)
    syllabus = Syllabus(path)

    assert syllabus.log == [
        'url',
        'provenance',
        'date',
        'checksum',
        'format'
    ]


def test_log_missing(mock_osp):

    """
    When the log is absent, return an empty list.
    """

    path = mock_osp.add_file()
    syllabus = Syllabus(path)

    os.remove(path+'.log')
    assert syllabus.log == []
