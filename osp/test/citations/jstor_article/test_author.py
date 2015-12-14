

import pytest

from osp.citations.jstor_article import JSTOR_Article


@pytest.mark.parametrize('inputs,authors', [

    (
        [
            ('David', 'McClure'),
            ('Joe', 'Karaganis'),
            ('Dennis', 'Tenen'),
        ],
        [
            'David McClure',
            'Joe Karaganis',
            'Dennis Tenen',
        ]
    ),

    # Empty given name -> retain surnames.
    (
        [
            ('', 'McClure'),
            ('Joe', 'Karaganis'),
            ('', 'Tenen'),
        ],
        [
            'McClure',
            'Joe Karaganis',
            'Tenen',
        ]
    ),

    # Missing given name -> retain surnames.
    (
        [
            (None, 'McClure'),
            ('Joe', 'Karaganis'),
            (None, 'Tenen'),
        ],
        [
            'McClure',
            'Joe Karaganis',
            'Tenen',
        ]
    ),

    # Empty surname -> omit author.
    (
        [
            ('David', ''),
            ('Joe', 'Karaganis'),
            ('Dennis', ''),
        ],
        [
            'Joe Karaganis',
        ]
    ),

    # Missing surname -> omit author.
    (
        [
            ('David', None),
            ('Joe', 'Karaganis'),
            ('Dennis', None),
        ],
        [
            'Joe Karaganis',
        ]
    ),

])
def test_author(inputs, authors, mock_jstor):

    path = mock_jstor.add_article(author=inputs)

    assert JSTOR_Article(path).author == authors
