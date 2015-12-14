

import pytest

from osp.citations.utils import clean_field


@pytest.mark.parametrize('raw,clean', [

    ('War and Peace', 'War and Peace'),

    # Strip whitespace.
    ('  War and Peace  ', 'War and Peace'),

    # Empty -> None.
    ('', None),
    ('  ', None),

])
def test_clean_field(raw, clean, mock_hlom):
    assert clean_field(raw) == clean
