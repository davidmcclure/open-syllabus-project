

from osp.common.utils import grouper


def test_even_groups():

    """
    When the total size of the iterable is evenly divided by the group size,
    all groups should be generated.
    """

    groups = grouper(range(50), 10)

    # Should generate 10 groups, each of length 10.
    assert list(next(groups)) == list(range(10))
    assert list(next(groups)) == list(range(10, 20))
    assert list(next(groups)) == list(range(20, 30))
    assert list(next(groups)) == list(range(30, 40))
    assert list(next(groups)) == list(range(40, 50))

    # And then stop.
    assert next(groups, False) == False


def test_uneven_groups():

    """
    When the group size doesn't evenly divide the iterable, all full-sized
    groups should be yielded, followed by a final group with the remainder.
    """

    groups = grouper(range(55), 10)

    # Should generate the 10 full-sized groups.
    assert list(next(groups)) == list(range(10))
    assert list(next(groups)) == list(range(10, 20))
    assert list(next(groups)) == list(range(20, 30))
    assert list(next(groups)) == list(range(30, 40))
    assert list(next(groups)) == list(range(40, 50))

    # And then the last 5 elements.
    assert list(next(groups)) == list(range(50, 55))

    # And then stop.
    assert next(groups, False) == False
