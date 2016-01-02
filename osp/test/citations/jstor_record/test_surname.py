

import pytest

from osp.citations.jstor_record import JSTOR_Record


@pytest.mark.parametrize('inputs,surname', [

    # Single author.
    (
        [
            ('David', 'McClure'),
        ],
        'McClure'
    ),

    # Multiple authors.
    (
        [
            ('David', 'McClure'),
            ('Joe', 'Karaganis'),
            ('Dennis', 'Tenen'),
        ],
        'McClure'
    ),

    # No authors.
    (
        [],
        None
    ),

])
def test_surname(inputs, surname, mock_jstor):

    path = mock_jstor.add_article(author=inputs)

    assert JSTOR_Record(path).surname == surname
