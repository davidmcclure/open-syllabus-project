

import re


def tokenize_query(title, author):

    """
    Extract normalized query tokens.

    Args:
        title (str): The text title.
        author (str): The text author.

    Returns:
        list: The cleaned tokens.
    """

    pattern = re.compile('[a-z]+')

    # Extract tokens.
    t_tokens = re.findall(pattern, title.lower())
    a_tokens = re.findall(pattern, author.lower())

    # Sort the author names.
    tokens = t_tokens + sorted(a_tokens)

    # Remove articles.
    tokens = [t for t in tokens if t not in ['a', 'an', 'the']]

    return tokens


def tokenize_field(value):

    """
    Extract normalized tokens from a field.

    Args:
        value (str): The field value.

    Returns:
        list: The cleaned tokens.
    """

    # Extract tokens.
    tokens = re.findall('[a-z]+', value.lower())

    # Remove articles.
    tokens = [t for t in tokens if t not in ['a', 'an', 'the']]

    return tokens
