

import math

from itertools import islice, chain
from clint.textui import progress


def query_bar(query):

    """
    Wrap a query in a progress bar.

    :param query: A query instance.
    """

    size = query.count()
    return progress.bar(query, expected_size=size)


def partitions(total, n, start=0):

    """
    Get start/stop boundaries for N partitions.

    :param total: The total number of objects.
    :param n: The number of partitions.
    :param start: The number to start from.
    """

    plen = math.ceil(total/n)

    bounds = []
    for i1 in range(start, total, plen):
        i2 = i1+plen-1 if i1+plen < total else total
        bounds.append((i1, i2))

    return bounds


def grouper(iterable, size):

    """
    Yield "groups" from an iterable.

    :param iterable: The iterable.
    :param size: The size of the group.
    """

    source = iter(iterable)

    while True:
        group = islice(source, size)
        yield chain([next(group)], group)
