

import pytest

from osp.citations.hlom_record import HLOM_Record


def test_authors(mock_hlom):

    record = mock_hlom.add_marc(author='David W. McClure')

    assert HLOM_Record(record).authors == ['David W. McClure']
