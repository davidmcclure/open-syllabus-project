

from osp.corpus.utils import int_to_dir


def segment_range(*args):

    """
    Generate a range of segment names.

    Args:
        s1 (int): The first segment.
        s2 (int): The last segment.

    Yields:
        str: The next segment name.
    """

    for i in range(*args):
        yield int_to_dir(i)
