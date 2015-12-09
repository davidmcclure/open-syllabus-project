

import re
import itertools
import pkgutil
import csv

from osp.common.utils import read_csv
from collections import OrderedDict


def normalize_field(query):

    """
    Normalize a field for querying.

    Args:
        query (str): The query string.

    Returns:
        str: The cleaned query.
    """

    # Remove non-letter characters, downcase, strip.
    letters = re.sub('[^a-z]', ' ', query.lower()).strip()

    # Collapse whitespace to a single space.
    return re.sub('\s{2,}', ' ', letters)


def prettify_field(field):

    """
    Clean a field for public-facing display - strip spaces and non-word
    characters from the beginning and end of the value.

    Args:
        field (str): The field value.

    Returns:
        str: The cleaned value.
    """

    punct = '^(?!\()[\W\s]+|(?!\))[\W\s]+$'
    return re.sub(punct, '', field) if field else None


def sort_dict(d, reverse=True):

    """
    Sort a dictionary (or OrderedDict) by value, descending.

    Args:
        d (dict): A dictionary.
        reverse (bool): If true, sort in descending order.

    Returns:
        OrderedDict: The sorted dictionary.
    """

    sort = sorted(d.items(), key=lambda x: x[1], reverse=reverse)
    return OrderedDict(sort)
