

import itertools
import re


def sanitize_query(query):

    """
    Escape Lucene-reserved characters:
    + - & | ! ( ) { } [ ] ^ " ~ * ? : \ /

    :param query: The query string.
    """

    return re.sub(
        '([\+\-\&\|\!\(\)\{\}\[\]\^\"\~\*\?\:\\\/])',
        r'\\\1',
        query
    )


def clean_field(field):

    """
    Clean a field for Elasticsearch - strip spaces and non-word characters
    from the beginning and end of the value.

    :param field: The field value.
    """

    punct = '^[\W\s]*|[\W\s]*$'
    return re.sub(punct, '', field) if field else None
