

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
            'journal': {
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

            yield dict(
                _id         = row.id,
                title       = row.title,
                author      = row.author,
                publisher   = row.publisher,
                date        = row.date,
                journal     = row.journal_title,
                url         = row.url,
            )


    @classmethod
    def materialize_ranking(cls, counts, query):
        pass
