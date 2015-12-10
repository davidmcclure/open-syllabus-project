

import pytest


def test_queries(add_text):

    """
    Text#queries should generate a set of Elasticsearch queries.
    """

    text = add_text(title='Anna Karenina', author='David William McClure')

    queries = text.queries

    # Title + complete name.
    assert 'anna karenina david william mcclure' in queries

    # Title + partial names.
    assert 'anna karenina david' in queries
    assert 'anna karenina william' in queries
    assert 'anna karenina mcclure' in queries
