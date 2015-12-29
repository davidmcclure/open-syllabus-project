

import pytest

from osp.corpus.syllabus import Syllabus


def test_domain(mock_osp):

    """
    Syllabus#domain should provide the parsed TLD.
    """

    path = mock_osp.add_file(log=dict(url='http://test.edu'))
    syllabus = Syllabus(path)

    assert syllabus.domain == 'test.edu'
