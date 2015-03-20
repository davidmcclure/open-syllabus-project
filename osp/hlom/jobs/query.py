

from osp.common.config import config
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation


def query(id):

    """
    Query a MARC record against the OSP corpus.

    :param id: The hlom_record row id.
    """

    row = HLOM_Record.get(HLOM_Record.id==id)

    # Execute the query.
    results = config.es.search('osp', 'syllabus', timeout=30, body={
        'fields': ['doc_id'],
        'size': 100000,
        'query': {
            'match_phrase': {
                'body': {
                    'query': row.query,
                    'slop': 10
                }
            }
        }
    })

    if results['hits']['total'] > 0:

        citations = []
        for hit in results['hits']['hits']:
            print(hit)
            citations.append({
                'document': hit['fields']['doc_id'][0],
                'record': row.id
            })

        # Write the citation links.
        HLOM_Citation.insert_many(citations).execute()


def queue_queries(id1, id2):

    """
    Queue HLOM query tasks in the worker.

    :param id1: The first id.
    :param id2: The last id.
    """

    queue = Queue(connection=redis)

    for i in range(id1, id2+1):
        queue.enqueue(query, i)
