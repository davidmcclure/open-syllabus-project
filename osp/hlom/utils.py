

import itertools
import re


def sanitize_query(query):

    """
    Scrub out Elasticsearch-reserved characters:
    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

    :param query: The query string.
    """

    return re.sub(
        '[\+\-\&\!\(\)\{\}\[\]\^\"\~\*\?\:\\\/]',
        '',
        query
    )
