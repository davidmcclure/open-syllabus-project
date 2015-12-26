

import pytest


pytestmark = pytest.mark.usefixtures('db')


@pytest.mark.parametrize('inputs', [

    # Coalesce formattings.
    [
        ('Anna Karenina', 'Leo Tolstoy'),
        ('ANNA KARENINA', 'LEO TOLSTOY'),
        ('"Anna Karenina."', '"Leo Tolstoy."'),
    ],

    # Ignore author name order.
    [
        ('Anna Karenina', 'Leo N. Tolstoy'),
        ('Anna Karenina', 'Tolstoy, Leo N.'),
        ('Anna Karenina', 'N. Tolstoy, Leo'),
    ],

])
def test_coalesce(inputs, add_text):

    hashes = set()

    for title, author in inputs:
        hashes.add(add_text(title=title, author=[author]).hash)

    assert len(hashes) == 1
