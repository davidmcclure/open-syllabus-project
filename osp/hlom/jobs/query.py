

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

    # Construct an ES query.
    query = sanitize_query(' '.join([
        record.title(),
        record.author()
    ]))

    results = es.search('osp', 'syllabus', {
        'fields': ['path'],
        'query': {
            'match_phrase': {
                'body': {
                    'query': query,
                    'slop': 10
                }
            }
        }
    })

    # TODO: Write the links.
    hits = results['hits']['total']
    if hits > 0:
        print(query)
        print(hits)
