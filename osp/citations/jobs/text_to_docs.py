

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


    doc_id_tokens = {}
    for tokens in row.queries:

        # Execute the query.
        results = config.es.search(

            index='document',
            timeout=30,

            body={
                'size': 100000,
                'filter': {
                    'query': {
                        'match_phrase': {
                            'body': {
                                'query': ' '.join(tokens),
                                'slop': 30,
                            }
                        }
                    }
                }
            }

        )

        if results['hits']['total'] > 0:
            for hit in results['hits']['hits']:

                # Get the doc id.
                doc_id = int(hit['_id'])

                # Map doc id -> tokens.
                matches = doc_id_tokens.setdefault(doc_id, set())
                matches.update(tokens)


    # Build doc -> text links.
    citations = []
    for doc_id, tokens in doc_id_tokens.items():

        citations.append({
            'document': doc_id,
            'text': row.id,
            'tokens': list(tokens),
        })

    # Bulk-insert the results.
    if citations:
        Citation.insert_many(citations).execute()
