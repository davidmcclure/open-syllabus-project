

from osp.fields.models.field import Field


def test_secondary_field():

    """
    Field#query_regexes() should build a query from the secondary field, when
    one is provided.
    """

    field = Field.create(secondary_field='History')

    assert field.query_regexes('{:s} regex') == [
        'History regex'
    ]


def test_abbreviations():

    """
    A query should be formed from each abbreviation.
    """

    field = Field.create(abbreviations=['AB', 'CD', 'EF'])

    assert field.query_regexes('{:s} regex') == [
        'AB regex',
        'CD regex',
        'EF regex',
    ]
