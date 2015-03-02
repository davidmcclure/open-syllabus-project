

from osp.common.utils import grouper


def test_even_groups():

    """
    When the total size of the iterable is evenly divided by the group size,
    all groups should be generated.
    """

    groups = grouper(range(100), 10)

    # Should generate 10 groups, each of length 10.
    for i in range(10):
        assert list(next(groups)) == list(range(i*10, (i*10)+10))

    # And then stop.
    assert next(groups, False) == False
