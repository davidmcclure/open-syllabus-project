

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
            'state': {
                'type': 'string'
            },
            'country': {
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

        for row in query_bar(Citation.select()):

            doc = {}

            # Local fields:

            doc['_id'] = row.id
            doc['text_id'] = row.text_id
            doc['document_id'] = row.document_id
            doc['corpus'] = row.text.corpus
            doc['min_freq'] = row.min_freq

            # Field references:

            subfield = row.subfield

            if subfield:
                doc['subfield_id'] = subfield.id
                doc['field_id'] = subfield.field_id

            # Institution reference:

            inst = row.institution

            if inst:
                doc['institution_id'] = inst.id
                doc['state'] = inst.state
                doc['country'] = inst.country

            yield doc


    @classmethod
    def rank_texts(cls, filters, min_freq=None, depth=1e6):

        """
        Given a set of query filters and a min_freq ceiling, count the number
        of times each text is cited on documents that match the criteria.

        Returns:
            dict: {'text_id' -> count}
        """

        # Assemble match filters.

        conds = []
        for field, value in filters.items():
            conds.append({
                'term': {
                    field: value
                }
            })

        # TODO: min_freq

        # Query for the aggregation.

        result = config.es.search(

            index = cls.es_index,
            doc_type = cls.es_doc_type,
            search_type = 'count',

            body = {
                'query': {
                    'bool': {
                        'must': conds
                    }
                },
                'aggs': {
                    'texts': {
                        'terms': {
                            'field': 'text_id',
                            'size': depth,
                        }
                    }
                }
            }

        )

        # Map text id -> citation count.

        counts = {}
        for b in result['aggregations']['texts']['buckets']:
            counts[str(b['key'])] = b['doc_count']

        return counts


    @classmethod
    def count_corpora(cls):
        pass


    @classmethod
    def count_subfields(cls):
        pass


    @classmethod
    def count_fields(cls):
        pass


    @classmethod
    def count_institutions(cls):
        pass


    @classmethod
    def count_states(cls):
        pass


    @classmethod
    def count_countries(cls):
        pass
