

from osp.fields.models import Subfield


def test_name(models):

    """
    Field#make_regex() should build a query from the field name.
    """

    field = Subfield.create(name='Field')

    assert field.make_regex('{:s} regex') == '(Field|FIELD) regex'


def test_abbreviations(models):

    """
    A query should be formed from each abbreviation.
    """

    field = Subfield.create(abbreviations=['AB', 'CD', 'EF'])

    assert field.make_regex('{:s} regex') == '(AB|CD|EF) regex'


def test_name_and_abbreviations(models):

    """
    When both are defined, make queries from the name + abbreviations.
    """

    field = Subfield.create(
        name='Field',
        abbreviations=['AB', 'CD', 'EF'],
    )

    assert field.make_regex('{:s} regex') == '(Field|FIELD|AB|CD|EF) regex'
