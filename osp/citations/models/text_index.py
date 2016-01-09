

import random

from osp.common import config
from osp.common.utils import query_bar, read_yaml
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.citations.models import Text, Citation

from clint.textui import progress


class Text_Index(Elasticsearch):


    es_index = 'text'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True,
        },
        'properties': {
            'corpus': {
                'type': 'string'
            },
            'identifier': {
                'type': 'string'
            },
            'title': {
                'type': 'string'
            },
            'authors': {
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

        query = (
            Text.select()
            .join(Citation)
            .where(Citation.valid==True)
        )

        for row in query_bar(query):

            yield dict(
                _id         = row.id,
                corpus      = row.corpus,
                identifier  = row.identifier,
                title       = row.pretty('title'),
                authors     = row.pretty('authors'),
                publisher   = row.pretty('publisher'),
                date        = row.pretty('date'),
                journal     = row.pretty('journal_title'),
                url         = row.url,
            )


    @classmethod
    def materialize_ranking(cls, ranks, query=None, size=1000):

        """
        Given a set of text counts, load texts sorted by count and apply a
        fulltext query, if provided.

        Args:
            ranks (dict): {'text_id' -> count}
            query (str): A free-text search query.
            size (int): The page length.

        Returns:
            dict: The Elasticsearch hits.
        """

        # Filter ids.

        conds = [{
            'ids': {
                'values': list(ranks.keys())
            }
        }]

        if query:
            conds.append({
                'multi_match': {
                    'query': query,
                    'type': 'phrase_prefix',
                    'fields': [
                        'title',
                        'authors',
                        'publisher',
                        'journal',
                    ],
                }
            })

        # Materialize the texts.

        result = config.es.search(

            index = cls.es_index,
            doc_type = cls.es_index,

            body = {
                'size': size,
                'query': {
                    'bool': {
                        'must': conds
                    }
                },
                'sort': {
                    '_script': {
                        'order': 'desc',
                        'type': 'number',
                        'script': 'ranks.get(doc["_id"].value)',
                        'params': {
                            'ranks': ranks
                        }
                    }
                },
                'highlight': {
                    'fields': {
                        'title': {
                            'number_of_fragments': 1,
                            'fragment_size': 1000
                        },
                        'authors': {
                            'number_of_fragments': 1,
                            'fragment_size': 1000
                        },
                        'publisher': {
                            'number_of_fragments': 1,
                            'fragment_size': 1000
                        },
                        'journal': {
                            'number_of_fragments': 1,
                            'fragment_size': 1000
                        }
                    }
                }
            }

        )

        return result['hits']


    @classmethod
    def materialize_corpus_facets(cls, counts):

        """
        Materialize corpus facet counts.

        Returns:
            dict: {label, value, count}
        """

        corpora = read_yaml(
            'osp.citations',
            'config/corpora.yml',
        )

        facets = []
        for slug, count in counts:

            facets.append(dict(
                label=corpora.get(slug),
                value=slug,
                count=count,
            ))

        return facets
