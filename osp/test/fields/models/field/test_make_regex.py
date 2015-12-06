

from osp.fields.models import Field


def test_secondary_field(models):

    """
    Field#make_regex() should build a query from the secondary field.
    """

    field = Field.create(secondary_field='Field')

    assert field.make_regex('{:s} regex') == '(Field|FIELD) regex'


def test_abbreviations(models):

    """
    A query should be formed from each abbreviation.
    """

    field = Field.create(abbreviations=['AB', 'CD', 'EF'])

    assert field.make_regex('{:s} regex') == '(AB|CD|EF) regex'


def test_secondary_field_and_abbreviations(models):

    """
    When both are defined, make queries from the secondary field and each
    abbreviation.
    """

    field = Field.create(
        secondary_field='Field',
        abbreviations=['AB', 'CD', 'EF'],
    )

    assert field.make_regex('{:s} regex') == '(Field|FIELD|AB|CD|EF) regex'
