

import itertools
import re


def sanitize_query(query):

    """
    Escape Lucene-reserved characters:

    Args:
        query (str): The query string.

    Returns:
        str: The cleaned query.
    """

    # Remove non-letter characters.
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
