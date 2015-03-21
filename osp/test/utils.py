

import hashlib

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


def sha1(value):

    """
    SHA1 a string.

    Args:
        value (str)
    """

    sha1 = hashlib.sha1()
    sha1.update(value.encode('utf8'))
    return sha1.hexdigest()
