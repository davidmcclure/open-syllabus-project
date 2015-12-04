

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

    parsed = []
    for abbr in abbrs.split(','):
        if abbr: parsed.append(abbr.strip())

    return parsed


def crunch(snippet):

    """
    Remove whitespace and linebreaks.

    Args:
        snippet (str): A text snippet.

    Returns:
        str: The crunched string.
    """

    return re.sub('\s{2,}', ' ', snippet).replace('\n', '')
