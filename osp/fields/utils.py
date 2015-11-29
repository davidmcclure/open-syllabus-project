

import re
import string


def clean_field_name(name):

    """
    Strip non-letters out of a field name

    Args:
        name (str): The field name.

    Returns:
        str: The cleaned name.
    """

    return name.strip(string.punctuation + string.whitespace)


def parse_abbrs(abbrs):

    """
    Parse comma-delimited abbreviations.

    Args:
        name (str): The raw abbreviations.

    Returns:
        list: The cleaned list.
    """

    # Strip trailing commas.
    abbrs = abbrs.strip(string.punctuation)

    # Strip spaces around edges.
    return list(map(lambda x: x.strip(), abbrs.split(',')))
