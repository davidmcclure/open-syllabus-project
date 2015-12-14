

import pytest

from osp.citations.hlom_record import HLOM_Record


@pytest.mark.parametrize('value,author', [

    ('David W. McClure', ['David W. McClure']),

    # Empty value -> empty list.
    ('', []),
    ('  ', []),

])
def test_author(value, author, mock_hlom):

    record = mock_hlom.add_marc(author=value)

    assert HLOM_Record(record).author == author
