

from osp.fields.utils import clean_field_name


def test_remove_punctuation():
    assert clean_field_name('Greek.') == 'Greek'


def test_strip_whitespace():
    assert clean_field_name('  Greek  ') == 'Greek'
    assert clean_field_name('\nGreek\n') == 'Greek'
