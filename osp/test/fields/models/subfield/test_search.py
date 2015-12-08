

import pytest

from osp.fields.models import Subfield


@pytest.mark.parametrize('text', [

    # 2-4 digits:

    'Field 12',
    'Field 123',
    'Field 1234',

    # Capitalized:

    'FIELD 101',

    # Dashes:

    'Field-101',
    'Field - 101',

    # Multiple spaces:

    'Field  101',

    # Wrapped:

    'abc Field 101 def',

])
def test_match_name(text, models, add_subfield):

    """
    Subfield#search() should match a field name code in the passed text.
    """

    subfield = add_subfield(name='Field')
    assert subfield.search(text) is not None


@pytest.mark.parametrize('text', [

    # 2-4 digits:

    'AB 12',
    'CD 12',
    'EF 12',

    'AB 123',
    'CD 123',
    'EF 123',

    'AB 1234',
    'CD 1234',
    'EF 1234',

    # Dashes:

    'AB-101',
    'CD-101',
    'EF-101',

    'AB - 101',
    'CD - 101',
    'EF - 101',

    # Multiple spaces:

    'AB  101',
    'CD  101',
    'EF  101',

    # Wrapped:

    'abc AB 101 def',
    'abc CD 101 def',
    'abc EF 101 def',

])
def test_match_abbreviations(text, models, add_subfield):

    """
    Should match abbreviated codes.
    """

    subfield = add_subfield(abbreviations=['AB', 'CD', 'EF'])
    assert subfield.search(text) is not None


def test_ignore_suffix_names(models, add_subfield):

    """
    Don't match names that are right-side suffixes of longer strings.
    """

    subfield = add_subfield(abbreviations=['NE'])
    assert subfield.search('KINE 101') is None
