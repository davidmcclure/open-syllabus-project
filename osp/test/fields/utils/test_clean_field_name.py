

import pytest

from osp.fields.utils import clean_field_name


@pytest.mark.parametrize('dirty,clean', [

    # Strip whitespace:
    ('  Field  ', 'Field'),
    ('\nField\n', 'Field'),

    # Keep interior spaces:
    ('Field Name', 'Field Name'),

    # Strip punctuation:
    ('Field.', 'Field'),

    # Keep interior spaces:
    ('Field-Name', 'Field-Name'),

])
def test_clean_field_name(dirty, clean):
    assert clean_field_name(dirty) == clean
