

import os

from osp.corpus.syllabus import Syllabus


def test_log_exists(corpus):

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

    path = corpus.add_file(log=log)
    syllabus = Syllabus(path)

    assert syllabus.log == [
        'url',
        'provenance',
        'date',
        'checksum',
        'format'
    ]


def test_log_missing(corpus):

    """
    When the log is absent, return an empty list.
    """

    path = corpus.add_file()
    syllabus = Syllabus(path)

    os.remove(path+'.log')
    assert syllabus.log == []
