

import pytest

from osp.citations.models import Text


@pytest.mark.parametrize('title,author,result', [

    # Title == surname
    ('Tolstoy', 'Tolstoy, Leo', True),

    # Title == first name
    ('Elvis', 'Presley, Elvis', True),
    ('Fidel', 'Castro, Fidel', True),

    # No overlap
    ('Tolstoy', 'War and Peace', False),

])
def test_title_and_author_overlap(title, author, result):

    text = Text(title=title, authors=[author])

    assert text.title_and_author_overlap == result
