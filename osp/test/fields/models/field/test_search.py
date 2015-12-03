

import pytest

from osp.fields.models.field import Field


def test_match_name(models):

    """
    Field#search() should match a field name code in the passed text.
    """

    field = Field.create(secondary_name='Field')

    assert field.search('Field 101') is not None


def test_match_abbreviations(models):

    """
    Should match abbreviated codes.
    """

    field = Field.create(abbreviations=['AB', 'CD', 'EF'])

    assert field.search('AB 101') is not None
    assert field.search('CD 101') is not None
    assert field.search('EF 101') is not None
