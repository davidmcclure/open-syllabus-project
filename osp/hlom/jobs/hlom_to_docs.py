

from osp.common.config import config
from osp.hlom.models.record import HLOM_Record
from osp.hlom.models.citation import HLOM_Citation


def hlom_to_docs(hlom_id):

    """
    Query a MARC record against the OSP corpus.

    :param hlom_id: The hlom_record row id.
    """

    row = HLOM_Record.get(HLOM_Record.id==hlom_id)

    # Execute the query.
    results = config.es.search('osp', 'document', timeout=30, body={
        'fields': ['doc_id'],
        'size': 100000,
        'filter': {
            'query': {
                'match_phrase': {
                    'body': {
                        'query': row.query,
                        'slop': 50
                    }
                }
            }
        }
    })

    if results['hits']['total'] > 0:

        citations = []
        for hit in results['hits']['hits']:
            citations.append({
                'document': hit['fields']['doc_id'][0],
                'record': row.id
            })

        # Write the citation links.
        HLOM_Citation.insert_many(citations).execute()
