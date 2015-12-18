

from osp.citations.models import Text
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.common.utils import query_bar


class Text_Index(Elasticsearch):


    es_index = 'osp'
    es_doc_type = 'text'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True,
        },
        'properties': {
            'title': {
                'type': 'string'
            },
            'author': {
                'type': 'string'
            },
            'publisher': {
                'type': 'string'
            },
            'date': {
                'type': 'string'
            },
            'journal_title': {
                'type': 'string'
            },
            'url': {
                'type': 'string'
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

        for row in query_bar(Text.select()):
            return {}
