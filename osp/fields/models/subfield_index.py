

from osp.fields.models import Subfield
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.common.utils import query_bar


class Subfield_Index(Elasticsearch):


    es_index = 'osp'
    es_doc_type = 'subfield'


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
        Index subfields.

        Yields:
            dict: The next document.
        """

        for row in query_bar(Subfield.select()):

            yield dict(
                _id = row.id,
                name = row.name,
            )
