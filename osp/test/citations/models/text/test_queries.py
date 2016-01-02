

import pytest

from osp.citations.utils import tokenize_field


pytestmark = pytest.mark.usefixtures('db')


def test_queries(add_text):

    """
    Text#queries should generate a set of Elasticsearch queries.
    """

    text = add_text(
        title='Anna Karenina',
        surname='Tolstoy'
    )

    queries = text.queries

    for tokens in [
        ['tolstoy', 'anna', 'karenina'],
        ['anna', 'karenina', 'tolstoy'],
    ]:

        assert tokens in queries
