

import pytest


@pytest.mark.parametrize('pairs', [

    # Coalesce formattings.
    [
        ('Anna Karenina', 'Leo Tolstoy'),
        ('anna karenina', 'leo tolstoy'),
        ('ANNA KARENINA', 'LEO TOLSTOY'),
        ('Anna  Karenina', 'Leo  Tolstoy'),
        (' Anna Karenina ', ' Leo Tolstoy '),
        ('Anna Karenina /', 'Leo Tolstoy /'),
        ('Anna Karenina.', 'Leo Tolstoy.'),
        ('"Anna Karenina,"', 'Leo Tolstoy'),
        ('Anna Karenina 2', 'Leo Tolstoy, 1828-1910'),
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
