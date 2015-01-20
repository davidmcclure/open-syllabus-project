

from osp.common.models.base import elasticsearch as es
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.utils import sanitize_query
from pymarc.record import Record


def query(control_number):

    """
    Query a MARC record against the OSP corpus.

    :param str control_number: The MARC identifier.
    """

    marc = HLOM_Record.get(
        HLOM_Record.control_number == control_number
    )

    # Hydrate a MARC record.
    record = Record(data=bytes(marc.record))

    # Form the query.
    query = record.title()
    if query and record.author():
        query += str(record.author())

    results = es.search('osp', 'syllabus', {
        'fields': ['path'],
        'query': {
            'query_string': {
                'query': sanitize_query(query)
            }
        }
    })

    print(sanitize_query(query))
    print(results['hits']['total'])
