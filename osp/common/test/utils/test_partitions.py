

from osp.common.utils import partitions


def test_no_remainder():

    """
    When the number of partitions evenly divides the total number of objects,
    partitions() should return evenly-spaced boundaries.
    """

    pts = partitions(50, 5)

    assert pts[0] == (0, 9)
    assert pts[1] == (10, 19)
    assert pts[2] == (20, 29)
    assert pts[3] == (30, 39)
    assert pts[4] == (40, 49)
