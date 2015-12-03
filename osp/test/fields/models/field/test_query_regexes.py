

from osp.fields.models.field import Field


def test_secondary_field(models):

    """
    Field#query_regexes() should build a query from the secondary field.
    """

    field = Field.create(secondary_field='Field')

    assert field.query_regexes('{:s} regex') == '(Field) regex'


def test_abbreviations(models):

    """
    A query should be formed from each abbreviation.
    """

    field = Field.create(abbreviations=['AB', 'CD', 'EF'])

    assert field.query_regexes('{:s} regex') == '(AB|CD|EF) regex'


def test_secondary_field_and_abbreviations(models):

    """
    When both are defined, make queries from the secondary field and each
    abbreviation.
    """

    field = Field.create(
        secondary_field='Field',
        abbreviations=['AB', 'CD', 'EF'],
    )

    assert field.query_regexes('{:s} regex') == '(Field|AB|CD|EF) regex'
