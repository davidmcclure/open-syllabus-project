

import regex
import iso3166
import us

from wordfreq import word_frequency


def clean_field(value):

    """
    Strip whitespace, cast empty -> None.

    Args:
        value (str): The field value.

    Returns:
        list: The cleaned tokens.
    """

    return (value.strip() or None) if value else None


def tokenize_field(value):

    """
    Extract normalized tokens from a field.

    Args:
        value (str): The field value.

    Returns:
        list: The cleaned tokens.
    """

    # Extract tokens.
    tokens = regex.findall('\p{L}{2,}', value.lower())

    # Remove articles.
    tokens = [t for t in tokens if t not in [
        'a', 'an', 'the', 'and',
    ]]

    return tokens


def get_text(tree, selector):

    """
    Extract text from an element. Return None if the element is missing or the
    value is empty.

    Args:
        tree (BeautifulSoup): A bs4 tree.
        selector (str): A CSS selector.

    Returns:
        str|None
    """

    tag = tree.select_one(selector)

    if tag:
        return tag.get_text(strip=True) or None

    else:
        return None


def get_attr(tree, selector, attr):

    """
    Extract an attribute value from an element. Return None if the element or
    attribute is missing, or the value is empty.

    Args:
        tree (BeautifulSoup): A bs4 tree.
        selector (str): A CSS selector.
        attr (str): An attribute name.

    Returns:
        str|None
    """

    tag = tree.select_one(selector)

    if tag:
        value = tag.attrs.get(attr, '').strip()
        return value or None

    else:
        return None


def is_toponym(value):

    """
    Is a string the name of a US state or country?

    Args:
        value (str)

    Returns: bool
    """

    return bool(
        iso3166.countries.get(value, None) or
        us.states.lookup(value)
    )
