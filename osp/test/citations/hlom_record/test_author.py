

import pytest

from osp.citations.hlom_record import HLOM_Record


def test_author(mock_hlom):

    record = mock_hlom.add_marc(author='David W. McClure')

    assert HLOM_Record(record).author == ['David W. McClure']
