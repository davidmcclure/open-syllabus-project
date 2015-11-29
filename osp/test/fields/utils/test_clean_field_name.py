

from osp.fields.utils import clean_field_name


def test_strip_whitespace():
    assert clean_field_name('  Field  ') == 'Field'
    assert clean_field_name('\nField\n') == 'Field'

def test_keep_interior_spaces():
    assert clean_field_name('Field Name') == 'Field Name'

def test_strip_punctuation():
    assert clean_field_name('Field.') == 'Field'

def test_keep_interior_punctuation():
    assert clean_field_name('Field-Name') == 'Field-Name'
