

from osp.common.config import config
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.common.utils import query_bar
from osp.fields.models import Field

from clint.textui import progress


class Field_Index(Elasticsearch):


    es_index = 'field'


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
    def es_stream_mock_docs(cls):

        """
        Stream (mock) Elasticsearch docs.

        Yields:
            dict: The next document.
        """

        for i in progress.bar(range(1, 31)):

            yield dict(
                _id = i,
                name = 'Field {0}'.format(i),
            )


    @classmethod
    def materialize_facets(cls, counts):

        """
        Materialize facet counts.

        Returns:
            dict: {label, value, count}
        """

        ids = [c[0] for c in counts]

        result = config.es.mget(
            index = cls.es_index,
            doc_type = cls.es_index,
            body = { 'ids': ids }
        )

        facets = []
        for i, doc in enumerate(result['docs']):

            facets.append(dict(
                label = doc['_source']['name'],
                value = int(doc['_id']),
                count = counts[i][1]
            ))

        return facets
