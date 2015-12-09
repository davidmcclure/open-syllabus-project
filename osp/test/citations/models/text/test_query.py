

import pytest


@pytest.mark.parametrize('inputs,query', [

    # Downcase.
    (
        [
            ('Anna Karenina', 'Leo Tolstoy'),
            ('anna karenina', 'leo tolstoy'),
            ('ANNA KARENINA', 'LEO TOLSTOY'),
        ],
        'anna karenina leo tolstoy'
    ),

    # Remove whitespace.
    (
        [
            ('Anna  Karenina', 'Leo  Tolstoy'),
            (' Anna Karenina ', ' Leo Tolstoy '),
            ('Anna Karenina\n', 'Leo Tolstoy\n'),
        ],
        'anna karenina leo tolstoy'
    ),

    # Remove punctuation.
    (
        [
            ('Anna Karenina /', 'Leo Tolstoy /'),
            ('Anna Karenina.', 'Leo Tolstoy.'),
            ('"Anna Karenina."', '"Leo Tolstoy."'),
        ],
        'anna karenina leo tolstoy'
    ),


    # # Ignore author order.
    # [
        # ('Anna Karenina', 'Leo Tolstoy'),
        # ('Anna Karenina', 'Tolstoy, Leo')
    # ],

    # # Ignore numbers.
    # [
        # ('Republic 5', 'Plato'),
        # ('Republic 10', 'Plato'),
        # ('Republic', 'Plato, 1564-1616')
    # ],

])
def test_query(inputs, query, add_text):

    for title, author in inputs:
        text = add_text(title=title, author=author)
        assert text.query == query
