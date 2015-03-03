

from osp.corpus.utils import int_to_dir


def segment_range(s1, s2):

    """
    Generate a range of segment names.

    Args:
        s1 (int): The first segment.
        s2 (int): The last segment.

    Yields:
        str: The next segment name.
    """

    for i in range(s1, s2):
        yield int_to_dir(i)
