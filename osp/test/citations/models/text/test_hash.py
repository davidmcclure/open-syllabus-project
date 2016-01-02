

import pytest


pytestmark = pytest.mark.usefixtures('db')


@pytest.mark.parametrize('dupes', [

    # Coalesce formattings.
    [
        ('Anna Karenina', 'Tolstoy'),
        ('ANNA KARENINA', 'TOLSTOY'),
        ('"Anna Karenina."', '"Tolstoy."'),
    ],

    # Ignore surname name order.
    [
        ('Anna Karenina', 'Nikolayevich Tolstoy'),
        ('Anna Karenina', 'Tolstoy Nikolayevich'),
    ],

])
def test_coalesce(dupes, add_text):

    hashes = set()

    for title, surname in dupes:
        hashes.add(add_text(title=title, surname=surname).hash)

    assert len(hashes) == 1
