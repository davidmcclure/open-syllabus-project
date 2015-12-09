

import pytest


def test_query(add_text):

    """
    Text#query should generate a plaintext query for Elasticsearch.
    """

    text = add_text(
        title='Anna Karenina',
        author='Leo Tolstoy',
    )

    assert text.query == 'anna karenina leo tolstoy'
