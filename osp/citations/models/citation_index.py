

from osp.common.config import config
from osp.common.utils import query_bar
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.citations.models import Citation


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
    def rank_texts(cls, filters={}, min_freq=None, depth=1e6):

        """
        Given a set of query filters and a min_freq ceiling, count the number
        of times each text is cited on documents that match the criteria.

        Args:
            filters (dict): A set of key -> value filters.
            min_freq (float): The highest allowable min_freq.
            depth (int): The max number of texts to rank.

        Returns:
            dict: {'text_id' -> count}
        """

        conds = []

        # Assemble match filters.

        for field, value in filters.items():
            conds.append({
                ('terms' if type(value) is list else 'term'): {
                    field: value
                }
            })

        # Filter out semantically-unfocused citations.

        if min_freq:
            conds.append({
                'range': {
                    'min_freq': {
                        'lte': min_freq
                    }
                }
            })

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
    def docs_with_text(cls, text_id, depth=1e6):

        """
        Given a text, get the set of documents that assign the text.

        Args:
            text_id (int)

        Returns:
            list: A set of document ids.
        """

        result = config.es.search(

            index = cls.es_index,
            doc_type = cls.es_doc_type,
            search_type = 'count',

            body = {
                'query': {
                    'term': {
                        'text_id': text_id
                    }
                },
                'aggs': {
                    'texts': {
                        'terms': {
                            'field': 'document_id',
                            'size': depth,
                        }
                    }
                }
            }

        )

        doc_ids = []
        for b in result['aggregations']['texts']['buckets']:
            doc_ids.append(b['key'])

        return doc_ids


    @classmethod
    def count_facets(cls, field, depth=1000):

        """
        Given a field, return a set of facet counts.

        Args:
            field (str)

        Returns:
            list: (value, count)
        """

        result = config.es.search(

            index = cls.es_index,
            doc_type = cls.es_doc_type,
            search_type = 'count',

            body = {
                'aggs': {
                    'texts': {
                        'terms': {
                            'field': field,
                            'size': depth,
                        }
                    }
                }
            }

        )

        counts = []
        for b in result['aggregations']['texts']['buckets']:
            counts.append((b['key'], b['doc_count']))

        return counts
