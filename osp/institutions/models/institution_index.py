

from osp.institutions.models import Institution
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.common.utils import query_bar


class Institution_Index(Elasticsearch):


    es_index = 'osp'
    es_doc_type = 'institution'


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
        Index institutions.

        Yields:
            dict: The next document.
        """

        for row in query_bar(Institution.select()):

            yield dict(
                _id = row.id,
                name = row.name,
            )


    @classmethod
    def institution_facets(cls):
        pass


    @classmethod
    def state_facets(cls):
        pass


    @classmethod
    def country_facets(cls):
        pass
