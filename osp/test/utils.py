

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

    if len(args) == 1:
        s1 = 0
        s2 = args[0]

    else:
        s1 = args[0]
        s2 = args[1]

    for i in range(s1, s2):
        yield int_to_dir(i)
