

import re


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
