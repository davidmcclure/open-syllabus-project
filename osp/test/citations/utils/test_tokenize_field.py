

import pytest

from osp.citations.utils import tokenize_field


@pytest.mark.parametrize('values,tokens', [

    # Downcase.
    (
        [
            'Anna Karenina',
            'anna karenina',
            'ANNA KARENINA',
        ],
        ['anna', 'karenina']
    ),

    # Ignore whitespace.
    (
        [
            'Leo  Tolstoy',
            '  Leo Tolstoy  ',
            '\nLeo Tolstoy\n',
        ],
        ['leo', 'tolstoy']
    ),

    # Ignore punctuation.
    (
        [
            'Anna Karenina /',
            'Anna Karenina.',
            '"Anna Karenina."',
        ],
        ['anna', 'karenina']
    ),

    # Ignore numbers.
    (
        [
            'Leo Tolstoy 5',
            'Leo Tolstoy, 1828-1910',

        ],
        ['leo', 'tolstoy']
    ),

    # Ignore articles and "and".
    (
        [
            'The War and Peace',
            'A War and Peace',
            'An War and Peace',

        ],
        ['war', 'peace']
    ),

    # Ignore single-character tokens (eg, initials).
    (
        [
            'Leo N. Tolstoy',
            'Leo N Tolstoy',

        ],
        ['leo', 'tolstoy']
    ),

    # Allow unicode characters.
    (
        [
            'Gabriel García Márquez',
        ],
        ['gabriel', 'garcía', 'márquez']
    ),

])
def test_tokenize_field(values, tokens, add_text):
    for value in values:
        assert tokenize_field(value) == tokens
