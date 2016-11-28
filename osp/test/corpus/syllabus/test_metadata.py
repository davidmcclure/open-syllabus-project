

import os

from osp.corpus.syllabus import Syllabus


def test_valid_index(mock_osp):

    """
    When an in-bounds offset is passed to Syllabus#metadata(), the value
    should be returned.
    """

    path = mock_osp.add_file()
    syllabus = Syllabus(path)

    assert syllabus.metadata(1) is not None


def test_invalid_index(mock_osp):

    """
    Return None when an out-of-bounds offset is passed.
    """

    path = mock_osp.add_file()
    syllabus = Syllabus(path)

    assert syllabus.metadata(10) is None


def test_url(mock_osp):

    """
    Syllabus#url should return the log URL.
    """

    path = mock_osp.add_file(log={'url': 'osp.org'})
    syllabus = Syllabus(path)

    assert syllabus.url() == 'osp.org'


def test_provenance(mock_osp):

    """
    Syllabus#provenance should return the log origin.
    """

    path = mock_osp.add_file(log={'provenance': 'pytest'})
    syllabus = Syllabus(path)

    assert syllabus.provenance() == 'pytest'


def test_retrieved_date(mock_osp):

    """
    Syllabus#retrieved_date should return the log date.
    """

    path = mock_osp.add_file(log={'date': 'now'})
    syllabus = Syllabus(path)

    assert syllabus.retrieved_date() == 'now'


def test_checksum(mock_osp):

    """
    Syllabus#checksum should return the log checksum.
    """

    path = mock_osp.add_file(log={'checksum': '123'})
    syllabus = Syllabus(path)

    assert syllabus.checksum() == '123'


def test_file_type(mock_osp):

    """
    Syllabus#file_type should return the log file type.
    """

    path = mock_osp.add_file(log={'format': 'text/plain'})
    syllabus = Syllabus(path)

    assert syllabus.file_type() == 'text/plain'
