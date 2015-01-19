

import itertools


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
