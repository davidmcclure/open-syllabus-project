

from osp.common.utils import query_bar
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.corpus.models import Document_Text


class Document_Index(Elasticsearch):


    es_index = 'osp'
    es_doc_type = 'document'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True,
        },
        'properties': {
            'body': {
                'type': 'string'
            },
        }
    }


    @classmethod
    def es_stream_docs(cls):

        """
        Index document texts.

        Yields:
            dict: The next document.
        """

        for row in query_bar(Document_Text.select()):

            yield {
                '_id': row.document_id,
                'body': row.text,
            }
