

import pytest

from osp.fields.utils import parse_abbrs


@pytest.mark.parametrize('raw,parsed', [

    # Split on comma:
    ('AB, CD, EF', ['AB', 'CD', 'EF']),

    # Strip whitespace:
    ('  AB, CD, EF  ', ['AB', 'CD', 'EF']),
    ('\nAB, CD, EF\n', ['AB', 'CD', 'EF']),

    # Keep interior space:
    ('AB CD, EF GH', ['AB CD', 'EF GH']),

    # Ignore trailing comma:
    ('AB, CD, EF,', ['AB', 'CD', 'EF']),

    # Empty string -> None:
    ('', None),
    (' ', None),

])
def test_parse_abbrs(raw, parsed):
    assert parse_abbrs(raw) == parsed
