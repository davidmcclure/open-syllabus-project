

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


    lowest = {}
    for query, min_freq in row.queries:

        # Execute the query.
        results = config.es.search('osp', 'document', timeout=30, body={
            'fields': ['doc_id'],
            'size': 100000,
            'filter': {
                'query': {
                    'match_phrase': {
                        'body': {
                            'query': query,
                            'slop': 20
                        }
                    }
                }
            }
        })

        if results['hits']['total'] > 0:

            for hit in results['hits']['hits']:

                doc_id = hit['fields']['doc_id'][0]

                # Get the lowest score.
                freq = lowest.get(doc_id)

                # If first match, or new score is lower, set id -> score.
                if not freq or min_freq < freq:
                    lowest[doc_id] = min_freq


    # Build doc -> text links.
    citations = []
    for doc_id, min_freq in lowest.items():

        citations.append({
            'document': doc_id,
            'text': row.id,
        })

    # Bulk-insert the results.
    if citations:
        Citation.insert_many(citations).execute()
