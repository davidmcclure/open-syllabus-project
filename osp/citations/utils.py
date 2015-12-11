

import re

from wordfreq import word_frequency


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


def get_min_freq(tokens, lang='en'):

    """
    Given a list of tokens, return the lowest frequency score.

    Args:
        tokens (str): A list of tokens.

    Returns:
        float: The lowest frequence.
    """

    return min([word_frequency(t, lang) for t in tokens])
