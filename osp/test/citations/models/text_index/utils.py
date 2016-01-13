

import numpy as np


def score(count, max_count):

    """
    Compute a teaching score.

    Args:
        count (int)
        max_count (int)

    Returns: int
    """

    return np.sqrt(count) / np.sqrt(max_count)
