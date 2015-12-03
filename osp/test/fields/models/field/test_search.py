

import pytest

from osp.fields.models.field import Field


@pytest.mark.parametrize('text', [
    'Field 12',
    'Field 123',
    'Field 1234',
])
def test_match_name(text, models):

    """
    Field#search() should match a field name code in the passed text.
    """

    field = Field.create(secondary_name='Field')
    assert field.search(text) is not None


@pytest.mark.parametrize('text', [

    'AB 12',
    'CD 12',
    'EF 12',

    'AB 123',
    'CD 123',
    'EF 123',

    'AB 1234',
    'CD 1234',
    'EF 1234',

])
def test_match_abbreviations(text, models):

    """
    Should match abbreviated codes.
    """

    field = Field.create(abbreviations=['AB', 'CD', 'EF'])
    assert field.search(text) is not None
