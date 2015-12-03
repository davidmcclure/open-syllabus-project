

from osp.fields.models.field import Field


def test_secondary_field(models):

    """
    Field#query_regexes() should build a query from the secondary field.
    """

    field = Field.create(secondary_field='History')

    assert field.query_regexes('{:s} regex') == [
        'History regex'
    ]


def test_abbreviations(models):

    """
    A query should be formed from each abbreviation.
    """

    field = Field.create(abbreviations=['AB', 'CD', 'EF'])

    assert field.query_regexes('{:s} regex') == [
        'AB regex',
        'CD regex',
        'EF regex',
    ]
