

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

    # Join title + author.
    query = ' '.join([title, author]).lower()

    # Split tokens.
    tokens = re.findall('[a-z]+', query)

    # Remove articles.
    tokens = [t for t in tokens if t not in ['a', 'an', 'the']]

    return tokens
