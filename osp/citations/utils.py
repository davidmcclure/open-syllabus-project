

import re

from wordfreq import word_frequency


def clean_field(value):

    """
    Strip whitespace, cast empty -> None.

    Args:
        value (str): The field value.

    Returns:
        list: The cleaned tokens.
    """

    return value.strip() or None


def tokenize_field(value):

    """
    Extract normalized tokens from a field.

    Args:
        value (str): The field value.

    Returns:
        list: The cleaned tokens.
    """

    # Extract tokens.
    tokens = re.findall('[a-z]{2,}', value.lower())

    # Remove articles.
    tokens = [t for t in tokens if t not in ['a', 'an', 'the']]

    return tokens


def get_min_freq(tokens, lang='en'):

    """
    Given a list of tokens, return the lowest frequency score.

    Args:
        tokens (str): A list of tokens.

    Returns:
        float: The lowest frequence.
    """

    return min([word_frequency(t, lang)*1e6 for t in tokens])
