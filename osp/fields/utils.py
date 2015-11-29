

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
