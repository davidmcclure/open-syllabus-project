

import pytest

from osp.citations.hlom_record import HLOM_Record


@pytest.mark.parametrize('author,surname', [

    # Surname, given.
    ('McClure, David W.', 'McClure'),

    # Single name.
    ('Plato', 'Plato'),

    # Compound surname.
    ('Van Buren, Martin', 'Van Buren'),

    # Missing.
    (None, None),

])
def test_author(author, surname, mock_hlom):

    record = mock_hlom.add_marc(author=author)

    assert HLOM_Record(record).surname() == surname
