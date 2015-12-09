

import numpy as np


def score(count, max):

    """
    Score a citation count.

    Args:
        count (int): The citation count of the text.
        max (int): The citation count of the most-cited text.

    Returns: float
    """

    return (np.log(count)/np.log(max))*10
