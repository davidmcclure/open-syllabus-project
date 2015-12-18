

from osp.citations.models import Citation
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.common.utils import query_bar


class Citation_Index(Elasticsearch):


    es_index = 'osp'
    es_doc_type = 'citation'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True,
        },
        'properties': {
            'text_id': {
                'type': 'integer'
            },
            'document_id': {
                'type': 'integer'
            },
            'corpus': {
                'type': 'string'
            },
            'min_freq': {
                'type': 'float'
            },
            'subfield_id': {
                'type': 'integer'
            },
            'field_id': {
                'type': 'integer'
            },
            'institution_id': {
                'type': 'integer'
            },
        }
    }


    @classmethod
    def es_stream_docs(cls):

        """
        Stream Elasticsearch docs.

        Yields:
            dict: The next document.
        """

        for row in query_bar(Citation.select()):
            yield row.es_doc
