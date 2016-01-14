

import pytest

from osp.citations.utils import tokenize_field
from osp.citations.models import Text


@pytest.mark.parametrize('title,blacklisted', [

    # Blacklisted
    ('Letter', True),
    ('The White House', True),

    # Partially blacklisted
    ('Letters Home', False),

    # Not in blacklist
    ('War and Peace', False),

])
def test_singular(title, blacklisted):

    titles = map(tokenize_field, [
        'letter',
        'the white house',
    ])

    text = Text(title=title)

    assert text.title_blacklisted(titles) == blacklisted
