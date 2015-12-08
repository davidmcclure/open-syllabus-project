

def test_name(add_subfield):

    """
    Subfield#make_regex() should build a query from the field name.
    """

    subfield = add_subfield(name='Field')

    assert subfield.make_regex('{:s} regex') == '(Field|FIELD) regex'


def test_name_and_abbreviations(add_subfield):

    """
    When both are defined, make queries from the name + abbreviations.
    """

    subfield = add_subfield(abbreviations=['AB', 'CD', 'EF'])

    assert subfield.make_regex('{:s} regex') == '(Field|FIELD|AB|CD|EF) regex'
