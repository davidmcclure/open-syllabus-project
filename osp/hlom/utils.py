

import itertools
import re


def groups(iterable, n):

    """
    Yield evenly-sized groups from an iterable.

    :param itr: An iterable.
    :param n: The group length.
    """

    it = iter(iterable)
    while True:
        group = tuple(itertools.islice(it, n))
        if not group: return
        yield group


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


def group_hash(record):

    """
    Get a "grouping" hash from a MARC record, for de-duping.

    :param record: A MARC record instance.
    """

    pass
