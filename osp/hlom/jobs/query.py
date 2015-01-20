

from osp.common.models.base import elasticsearch as es
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
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

    # Execute the query.
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

    if results['hits']['total'] > 0:

        citations = []
        for hit in results['hits']['hits']:
            citations.append({
                'document': hit['fields']['path'],
                'record': control_number
            })

        # Write the citation links.
        HLOM_Citation.insert_many(citations).execute()
