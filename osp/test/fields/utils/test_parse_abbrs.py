

from osp.fields.utils import parse_abbrs


def test_split_on_comma():
    assert parse_abbrs('AB, CD, EF') == ['AB', 'CD', 'EF']

def test_strip_whitespace():
    assert parse_abbrs('  AB, CD, EF  ') == ['AB', 'CD', 'EF']
    assert parse_abbrs('\nAB, CD, EF\n') == ['AB', 'CD', 'EF']

def test_keep_interior_spaces():
    assert parse_abbrs('AB CD, EF GH') == ['AB CD', 'EF GH']

def test_ignore_trailing_comma():
    assert parse_abbrs('AB, CD, EF,') == ['AB', 'CD', 'EF']

def test_parse_empty_string_to_empty_array():
    assert parse_abbrs('') == []
