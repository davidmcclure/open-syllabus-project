

import pytest


@pytest.mark.parametrize('pairs', [

    # Coalesce formatting.
    [
        ('Anna Karenina', 'Leo Tolstoy'),
        ('ANNA KARENINA', 'LEO TOLSTOY'),
    ],

    # Ignore name order.
    [
        ('Anna Karenina', 'Leo Tolstoy'),
        ('Anna Karenina', 'Tolstoy, Leo'),
    ],

])
def test_hash(pairs, add_text):

    hashes = set()

    for title, author in pairs:
        hashes.add(add_text(title=title, author=author).hash)

    assert len(hashes) == 1
