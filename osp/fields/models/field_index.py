

from osp.fields.models import Field
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.common.utils import query_bar


class Field_Index(Elasticsearch):


    es_index = 'osp'
    es_doc_type = 'field'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True,
        },
        'properties': {
            'name': {
                'type': 'string'
            },
        }
    }


    @classmethod
    def es_stream_docs(cls):

        """
        Index fields.

        Yields:
            dict: The next document.
        """

        for row in query_bar(Field.select()):

            yield dict(
                _id = row.id,
                name = row.name,
            )


    @classmethod
    def field_facets(cls):
        pass
