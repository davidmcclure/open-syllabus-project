

import math


def paginate_query(query, n):

    """
    Paginate through all rows in a query result.

    :param query: A query instance.
    :param n: The number of rows per page.
    """

    page_count = math.ceil(query.count()/n)

    for page in range(1, page_count+1):
        for row in query.paginate(page, n).naive().iterator():
            yield row


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
