

import pytest


@pytest.mark.parametrize('pairs', [

    # Ignore capitalization.
    [
        ('Anna Karenina', 'Leo Tolstoy'),
        ('anna karenina', 'leo tolstoy'),
        ('ANNA KARENINA', 'LEO TOLSTOY')
    ],

    # Ignore whitespace.
    [
        ('Anna  Karenina', 'Leo  Tolstoy'),
        (' Anna Karenina ', ' Leo Tolstoy ')
    ],

    # Ignore punctuation.
    [
        ('Anna Karenina /', 'Leo Tolstoy /'),
        ('Anna Karenina.', 'Leo Tolstoy.'),
        ('"Anna Karenina,"', 'Leo Tolstoy')
    ],

    # Ignore articles.
    [
        ('The Republic', 'Plato'),
        ('A Republic', 'Plato'),
        ('An Republic"', 'Plato')
    ],

    # Ignore author order.
    [
        ('Anna Karenina', 'Leo Tolstoy'),
        ('Anna Karenina', 'Tolstoy, Leo')
    ],

    # Ignore numbers.
    [
        ('Republic 5', 'Plato'),
        ('Republic 10', 'Plato'),
        ('Republic', 'Plato, 1564-1616')
    ],

])
def test_hash(pairs, add_hlom):

    hashes = set()
    for p in pairs: hashes.add(add_hlom(p[0], p[1]).hash)
    assert len(hashes) == 1
