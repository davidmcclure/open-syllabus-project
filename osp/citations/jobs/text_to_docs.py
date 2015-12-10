

from osp.common.config import config
from osp.citations.models import Text
from osp.citations.models import Citation


def text_to_docs(text_id):

    """
    Query a text against the OSP corpus.

    Args:
        text_id (int): A text row id.
    """

    row = Text.get(Text.id==text_id)

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
                'text': row.id
            })

        # Write the citation links.
        Citation.insert_many(citations).execute()
