

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


def crunch(snippet):

    """
    Remove whitespace and linebreaks.

    Args:
        snippet (str): A text snippet.

    Returns:
        str: The crunched string.
    """

    return re.sub('\s{2,}', ' ', snippet).replace('\n', '')


def parse_abbrs(abbrs):

    """
    Parse comma-delimited abbreviations.

    Args:
        abbrs (str): The raw abbreviations.

    Returns:
        list: The cleaned list.
    """

    parsed = []
    for abbr in abbrs.split(','):
        if abbr.strip():
            parsed.append(abbr.strip())

    return parsed if len(parsed) else None


def filter_abbrs(abbrs, blacklist=[
    'JAN',
    'FEB',
    'MAR',
    'MAR',
    'APR',
    'MAY',
    'JUN',
    'JUL',
    'AUG',
    'SEP',
    'OCT',
    'NOV',
    'DEC',
]):

    """
    Filter out semantically-unfocused abbreviations.

    Args:
        abbrs (list): The parsed abbreviations.
        blacklist (list): Abbreviations to be removed.

    Returns:
        list: The filtered list.
    """

    return [a for a in abbrs if a not in blacklist]
