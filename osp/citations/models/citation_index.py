

import random
import numpy as np
import us
import iso3166

from osp.common import config
from osp.common.utils import query_bar
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.citations.models import Text, Citation

from scipy.stats import rankdata
from clint.textui import progress


class Citation_Index(Elasticsearch):

    es_index = 'citation'

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
                'index': 'not_analyzed',
                'type': 'string',
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
                'index': 'not_analyzed',
                'type': 'string',
            },
            'country': {
                'index': 'not_analyzed',
                'type': 'string',
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

        query = (
            Citation.select()
            .join(Text)
            .where(Text.display==True)
            .where(Text.valid==True)
        )

        for row in query_bar(query):

            doc = {}

            # Local fields:

            doc['_id'] = row.id
            doc['text_id'] = row.text_id
            doc['document_id'] = row.document_id
            doc['corpus'] = row.text.corpus

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
    def compute_ranking(cls, filters={}, depth=1e5):

        """
        Given a set of query filters, count the number of times each text is
        cited on documents that match the criteria.

        Args:
            filters (dict): A set of key -> value filters.
            depth (int): The max number of texts to rank.

        Returns:
            dict: {'text_id' -> count}
        """

        conds = []

        # Assemble match filters.

        for field, value in filters.items():

            if value: # Ignore empty values.

                conds.append({
                    ('terms' if type(value) is list else 'term'): {
                        field: value
                    }
                })

        # Query for the aggregation.

        result = config.es.search(

            index = cls.es_index,
            doc_type = cls.es_index,
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
    def docs_with_text(cls, text_id, depth=1000):

        """
        Given a text, get the set of documents that assign the text.

        Args:
            text_id (int)

        Returns:
            list: A set of document ids.
        """

        result = config.es.search(

            index = cls.es_index,
            doc_type = cls.es_index,
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
    def count_facets(cls, field, depth=100, include=None):

        """
        Given a field, return a set of facet counts.

        Args:
            field (str)
            depth (int)
            include (list)

        Returns:
            list: (value, count)
        """

        result = config.es.search(

            index = cls.es_index,
            doc_type = cls.es_index,
            search_type = 'count',

            body = {
                'aggs': {
                    'ranking': {
                        'terms': {
                            'field': field,
                            'size': depth,
                        }
                    },
                    'include': {
                        'terms': {
                            'field': field,
                            'include': include or [],
                        }
                    },
                }
            }

        )

        counts = {}

        # Merge the raw rankings + include list.
        for agg in ['ranking', 'include']:
            for b in result['aggregations'][agg]['buckets']:
                counts[b['key']] = (b['key'], b['doc_count'])

        # Sort by count descending.
        return sorted(
            list(counts.values()),
            key=lambda x: x[1],
            reverse=True,
        )

    @classmethod
    def compute_scores(cls, *args, **kwargs):

        """
        Compute "percentile" scores for texts - text X is assigned more
        frequently than Y percent of all texts.

        Args:
            depth (int): The max number of texts to rank.

        Returns:
            dict: {'text_id' -> count}
        """

        # Pull unfiltered counts.
        counts = cls.compute_ranking(*args, **kwargs)

        # Get the max count.
        max_count = max(list(counts.values()))

        return {
            tid: np.sqrt(count) / np.sqrt(max_count)
            for tid, count in counts.items()
        }
