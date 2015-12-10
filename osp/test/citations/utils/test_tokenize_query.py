

import pytest

from osp.citations.utils import tokenize_query


@pytest.mark.parametrize('inputs,tokens', [

    # Downcase.
    (
        [
            ('Anna Karenina', 'Leo Tolstoy'),
            ('anna karenina', 'leo tolstoy'),
            ('ANNA KARENINA', 'LEO TOLSTOY'),
        ],
        ['anna', 'karenina', 'leo', 'tolstoy']
    ),

    # Remove whitespace.
    (
        [
            ('Anna   Karenina', 'Leo   Tolstoy'),
            (' Anna Karenina ', ' Leo Tolstoy '),
            ('Anna Karenina\n', 'Leo Tolstoy\n'),
        ],
        ['anna', 'karenina', 'leo', 'tolstoy']
    ),

    # Remove punctuation.
    (
        [
            ('Anna Karenina /', 'Leo Tolstoy /'),
            ('Anna Karenina.', 'Leo Tolstoy.'),
            ('"Anna Karenina."', '"Leo Tolstoy."'),
        ],
        ['anna', 'karenina', 'leo', 'tolstoy']
    ),

    # Remove numbers.
    (
        [
            ('Republic 5', 'Plato'),
            ('Republic 10', 'Plato'),
            ('Republic', 'Plato, 1564-1616'),
        ],
        ['republic', 'plato']
    ),

    # Remove articles.
    (
        [
            ('The Republic', 'Plato'),
            ('A Republic', 'Plato'),
            ('An Republic', 'Plato'),
        ],
        ['republic', 'plato']
    ),

    # Sort author names.
    (
        [
            ('Anna Karenina', 'Leo Tolstoy'),
            ('Anna Karenina', 'Tolstoy, Leo'),
        ],
        ['anna', 'karenina', 'leo', 'tolstoy']
    ),

])
def test_tokenize_query(inputs, tokens, add_text):
    for title, author in inputs:
        assert tokenize_query(title, author) == tokens
