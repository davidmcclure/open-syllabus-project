

import pytest

from osp.fields.models.field import Field


@pytest.mark.parametrize('text', [

    # 2-4 digits:

    'Field 12',
    'Field 123',
    'Field 1234',

    # Ignore caps:

    'FIELD 101',

    # Dashes:

    'Field-101',
    'Field - 101',

    # Multiple spaces:

    'Field  101',

])
def test_match_name(text, models):

    """
    Field#search() should match a field name code in the passed text.
    """

    field = Field.create(secondary_name='Field')
    assert field.search(text) is not None


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

])
def test_match_abbreviations(text, models):

    """
    Should match abbreviated codes.
    """

    field = Field.create(abbreviations=['AB', 'CD', 'EF'])
    assert field.search(text) is not None
