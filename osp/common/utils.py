

import math


def paginate(query, n):

    """
    Paginate through all rows in a query result.

    :param query: A query instance.
    :param n: The number of rows per page.
    """

    page_count = math.ceil(query.count()/n)

    for page in range(page_count):
        for row in query.paginate(page, n).naive().iterator():
            yield row
