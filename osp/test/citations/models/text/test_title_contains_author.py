

import pytest

from osp.citations.models import Text


@pytest.mark.parametrize('surname,title,result', [

    # Surname subset of title
    ('Tolstoy', 'Leo Tolstoy', True),
    ('Tolstoy', 'Tolstoy, Leo', True),

    # Surname == title
    ('Tolstoy', 'Tolstoy', True),

    # Multi-token surname
    ('Von Braun', 'Wernher von Braun at NASA', True),

    ('Tolstoy', 'War and Peace', False),

])
def test_title_contains_author(surname, title, result):

    text = Text(surname=surname, title=title)

    assert text.title_contains_author == result
