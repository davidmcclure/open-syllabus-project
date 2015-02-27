

import os

from osp.corpus.syllabus import Syllabus


def test_valid_index(corpus):

    """
    When an in-bounds offset is passed to Syllabus#metadata(), the value
    should be returned.
    """

    path = corpus.add_file()
    syllabus = Syllabus(path)

    assert syllabus.metadata(1) is not None


def test_invalid_index(corpus):

    """
    Return None when an out-of-bounds offset is passed.
    """

    path = corpus.add_file()
    syllabus = Syllabus(path)

    assert syllabus.metadata(10) is None


def test_url(corpus):

    """
    Syllabus#url should return the log URL.
    """

    path = corpus.add_file(log={'url': 'osp.org'})
    syllabus = Syllabus(path)

    assert syllabus.url == 'osp.org'


def test_provenance(corpus):

    """
    Syllabus#provenance should return the log provenance.
    """

    path = corpus.add_file(log={'provenance': 'pytest'})
    syllabus = Syllabus(path)

    assert syllabus.provenance == 'pytest'


def test_date(corpus):

    """
    Syllabus#date should return the log date.
    """

    path = corpus.add_file(log={'date': 'now'})
    syllabus = Syllabus(path)

    assert syllabus.date == 'now'


def test_checksum(corpus):

    """
    Syllabus#checksum should return the log checksum.
    """

    path = corpus.add_file(log={'checksum': '123'})
    syllabus = Syllabus(path)

    assert syllabus.checksum == '123'


def test_file_type(corpus):

    """
    Syllabus#file_type should return the log file type.
    """

    path = corpus.add_file(log={'format': 'text/plain'})
    syllabus = Syllabus(path)

    assert syllabus.file_type == 'text/plain'
