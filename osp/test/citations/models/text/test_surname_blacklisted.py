

import pytest

from osp.citations.utils import tokenize_field
from osp.citations.models import Text


@pytest.mark.parametrize('surname,blacklisted', [

    # Blacklisted
    ('May', True),
    ('World Bank', True),

    # Partially blacklisted
    ('May-Weisman', False),

    # Not in blacklist
    ('Weisman', False),

])
def test_singular(surname, blacklisted):

    surnames = map(tokenize_field, [
        'may',
        'world bank',
    ])

    text = Text(surname=surname)

    assert text.surname_blacklisted(surnames) == blacklisted
