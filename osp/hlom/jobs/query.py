

from osp.common.models.base import redis, elasticsearch as es
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.utils import sanitize_query
from pymarc.record import Record
from rq import Queue


def query(id):

    """
    Query a MARC record against the OSP corpus.

    :param id: The hlom_record row id.
    """

    row = HLOM_Record.get(HLOM_Record.id==id)

    # Hydrate a MARC record.
    marc = row.pymarc_record()

    # Construct an ES query.
    query = sanitize_query(' '.join([
        marc.title(),
        marc.author()
    ]))

    # Execute the query.
    results = es.search('osp', 'syllabus', timeout=30, body={
        'fields': [],
        'size': 100000,
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
                'document': hit['_id'],
                'record': row.control_number
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
