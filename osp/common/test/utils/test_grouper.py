

from osp.common.utils import grouper


def test_even_groups():

    """
    When the total size of the iterable is evenly divided by the group size,
    all groups should be generated.
    """

    groups = grouper(range(100), 10)

    # Should generate 10 groups, each of length 10.
    assert list(next(groups)) == list(range(0, 10))
    assert list(next(groups)) == list(range(10, 20))
    assert list(next(groups)) == list(range(20, 30))
    assert list(next(groups)) == list(range(30, 40))
    assert list(next(groups)) == list(range(40, 50))
    assert list(next(groups)) == list(range(50, 60))
    assert list(next(groups)) == list(range(60, 70))
    assert list(next(groups)) == list(range(70, 80))
    assert list(next(groups)) == list(range(80, 90))
    assert list(next(groups)) == list(range(90, 100))

    # And then stop.
    assert next(groups, False) == False


def test_uneven_groups():

    """
    When the group size doesn't evenly divide the iterable, all full-sized
    groups should be yielded, followed by a final group with the remainder.
    """

    groups = grouper(range(105), 10)

    # Should generate the 10 full-sized groups.
    assert list(next(groups)) == list(range(0, 10))
    assert list(next(groups)) == list(range(10, 20))
    assert list(next(groups)) == list(range(20, 30))
    assert list(next(groups)) == list(range(30, 40))
    assert list(next(groups)) == list(range(40, 50))
    assert list(next(groups)) == list(range(50, 60))
    assert list(next(groups)) == list(range(60, 70))
    assert list(next(groups)) == list(range(70, 80))
    assert list(next(groups)) == list(range(80, 90))
    assert list(next(groups)) == list(range(90, 100))

    # And then the last 5 elements.
    assert list(next(groups)) == list(range(100, 105))

    # And then stop.
    assert next(groups, False) == False
