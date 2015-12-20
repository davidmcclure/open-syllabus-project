

import random
import requests
import re

from osp.common.config import config
from osp.common.mixins.elasticsearch import Elasticsearch

from clint.textui import progress


class Faker:


    def __init__(self, text_url='http://goo.gl/OJR4J0'):

        """
        Load and clean a text URL.

        Args:
            text_url (str)
        """

        r = requests.get(text_url)
        self.text = re.sub('\s{2,}', ' ', r.text).strip()


    def snippet(self, length):

        """
        Get a random text snippet.

        Args:
            length (int)
        """

        start = random.randrange(0, len(self.text)-length)
        return self.text[start:start+length]


class Citation_Index(Elasticsearch):


    es_index = 'osp'
    es_doc_type = 'citation'


    es_mapping = {
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

        for i in progress.bar(range(1000000)):

            yield dict(
                _id             = i,
                text_id         = random.randint(1, 200000),
                document_id     = random.randint(1, 1500000),
                corpus          = random.choice(['hlom', 'jstor']),
                min_freq        = random.uniform(0, 10),
                institution_id  = random.randint(0, 1000),
                field_id        = random.randint(0, 10),
                subfield_id     = random.randint(0, 200),
            )


    @classmethod
    def aggregate(cls, filters, size=1000000):

        """
        Given a set of filters, map text ids -> counts.

        Returns: dict
        """

        must = []

        for field, value in filters.items():
            must.append({'term': {
                field: value
            }})

        body = {
            'query': {
                'bool': {
                    'must': must
                }
            },
            'aggs': {
                'texts': {
                    'terms': {
                        'field': 'text_id',
                        'size': size,
                    }
                }
            }
        }

        result = config.es.search(
            search_type = 'count',
            index = cls.es_index,
            doc_type = cls.es_doc_type,
            body = body,
        )

        counts = {}
        for b in result['aggregations']['texts']['buckets']:
            counts[str(b['key'])] = b['doc_count']

        return counts


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
        }
    }


    @classmethod
    def es_stream_docs(cls):

        """
        Stream Elasticsearch docs.

        Yields:
            dict: The next document.
        """

        faker = Faker()

        for i in progress.bar(range(200000)):

            yield dict(
                _id         = i,
                title       = faker.snippet(100),
                author      = faker.snippet(40),
                publisher   = faker.snippet(60),
            )


    @classmethod
    def materialize(cls, counts, q=None, size=1000):

        """
        Given a text id -> count map and a free text query, materialize an
        ordered result set.

        Returns: list
        """

        must = [{
            'ids': {
                'values': list(counts.keys())
            },
        }]

        if q: must.append({
            'multi_match': {
                'query': q,
                'fields': ['title', 'author', 'publisher'],
                'type': 'phrase_prefix'
            },
        })

        query = {
            'bool': {
                'must': must
            }
        }

        body = {
            'size': size,
            'query': query,
            'sort': {
                '_script': {
                    'type': 'string',
                    'order': 'desc',
                    'script': 'counts.get(doc["_id"].value)',
                    'params': {
                        'counts': counts
                    }
                }
            },
            'highlight': {
                'fields': {
                    'title': {
                        'number_of_fragments': 1,
                        'fragment_size': 1000
                    },
                    'author': {
                        'number_of_fragments': 1,
                        'fragment_size': 1000
                    },
                    'publisher': {
                        'number_of_fragments': 1,
                        'fragment_size': 1000
                    }
                }
            }
        }

        return config.es.search(
            index = cls.es_index,
            doc_type = cls.es_doc_type,
            body = body,
        )


def query(filters, q=None, size=1000):
    counts = Citation_Index.aggregate(filters)
    return Text_Index.materialize(counts, q=q, size=size)
