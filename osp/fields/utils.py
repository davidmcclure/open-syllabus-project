

import re


def clean_field_name(name):

    """
    Strip non-letters out of a field name

    Args:
        name (str): The field name.

    Returns:
        str: The cleaned name.
    """

    return re.sub('[^a-zA-Z]', '', name).strip()
