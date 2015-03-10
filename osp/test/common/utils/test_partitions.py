

from osp.common.utils import partitions


def test_partitions():

    """
    partitions() should return boundaries for a set of N equally-sized
    partitions on an inclusive range.
    """

    pts = partitions(1, 100, 5)

    # Should produce 5 partitions.
    assert len(pts) == 5

    # Should start with 1, stop with 100.
    assert pts[0][0] == 1
    assert pts[-1][1] == 100

    # Should be adjacent.
    assert pts[0][1]+1 == pts[1][0]
    assert pts[1][1]+1 == pts[2][0]
    assert pts[2][1]+1 == pts[3][0]
    assert pts[3][1]+1 == pts[4][0]
