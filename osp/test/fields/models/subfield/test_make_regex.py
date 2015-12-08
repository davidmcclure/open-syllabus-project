

from osp.fields.models import Subfield


def test_name(models):

    """
    Subfield#make_regex() should build a query from the field name.
    """

    subfield = Subfield.create(name='Field')

    assert subfield.make_regex('{:s} regex') == '(Field|FIELD) regex'


def test_name_and_abbreviations(models):

    """
    When both are defined, make queries from the name + abbreviations.
    """

    subfield = Subfield.create(
        name='Field',
        abbreviations=['AB', 'CD', 'EF'],
    )

    assert subfield.make_regex('{:s} regex') == '(Field|FIELD|AB|CD|EF) regex'
