

import itertools
import re


def sanitize_query(query):

    """
    Scrub out Elasticsearch-reserved characters:
    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

    :param query: The query string.
    """

    return re.sub(
        '[\+\-\&\!\(\)\{\}\[\]\^\"\~\*\?\:\\\/]',
        '',
        query
    )


def clean_field(field):

    """
    Clean a field for Elasticsearch - strip spaces and non-word characters
    from the beginning and end of the value.

    :param field: The field value.
    """

    return re.sub('^[\W\s]*|[\W\s]*$', '', field)
