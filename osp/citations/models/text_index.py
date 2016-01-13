

import numpy as np
import random

from osp.common import config
from osp.common.utils import query_bar, read_yaml
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.citations.models import Text, Citation

from clint.textui import progress
from peewee import fn
from scipy.stats import rankdata


class Text_Index(Elasticsearch):


    es_index = 'text'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True,
        },
        'properties': {

            'corpus': {
                'index': 'not_analyzed',
                'type': 'string'
            },
            'identifier': {
                'index': 'not_analyzed',
                'type': 'string'
            },
            'count': {
                'type': 'integer'
            },
            'rank': {
                'type': 'integer'
            },
            'score': {
                'type': 'float'
            },

            'authors': {
                'type': 'string'
            },
            'title': {
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
    def rank_texts(cls):

        """
        Get total citation counts and ranks for texts.

        Returns: list
        """

        count = fn.Count(Citation.id)

        query = (
            Text
            .select(Text, count)
            .join(Citation)
            .where(Citation.valid==True)
            .group_by(Text.id)
            .order_by(Text.id)
            .naive()
        )

        # Get counts and ranks.
        counts = [t.count for t in query]
        ranks = rankdata(counts, 'max')

        # Compute exponentially-scaled count ratios.
        max_count = max(counts)
        scores = [np.sqrt(c)/np.sqrt(max_count) for c in counts]

        # Flip the ranks (#1 is most frequent).
        max_rank = max(ranks)
        ranks = [int(max_rank-r+1) for r in ranks]

        return [
            dict(zip(['text', 'rank', 'score'], t))
            for t in zip(query, ranks, scores)
        ]


    @classmethod
    def es_stream_docs(cls):

        """
        Stream Elasticsearch docs.

        Yields:
            dict: The next document.
        """

        for t in progress.bar(cls.rank_texts()):

            text = t['text']

            yield dict(

                _id         = text.id,
                corpus      = text.corpus,
                identifier  = text.identifier,
                count       = text.count,
                rank        = t['rank'],
                score       = t['score'],

                authors     = text.pretty('authors'),
                title       = text.pretty('title'),
                publisher   = text.pretty('publisher'),
                date        = text.pretty('date'),
                journal     = text.pretty('journal_title'),
                url         = text.url,

            )


    @classmethod
    def materialize_ranking(cls, ranks=None, query=None, size=1000):

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

        conds = []

        # If a query is provided, search text metadata.

        if query:

            conds.append({
                'simple_query_string': {
                    'query': query,
                    'default_operator': 'and',
                    'fields': [
                        'title',
                        'authors',
                        'publisher',
                        'journal',
                    ],
                }
            })

        # If a text -> count map is provided, only match filtered ids and sort
        # the results on the filtered counts.

        if ranks:

            conds.append({
                'ids': {
                    'values': list(ranks.keys())
                }
            })

            sort = {
                '_script': {
                    'order': 'desc',
                    'type': 'number',
                    'script': 'ranks.get(doc["_id"].value)',
                    'params': {
                        'ranks': ranks
                    }
                }
            }

        # If no ranks are provided, sort on the overall counts.

        else:

            sort = {
                'count': {
                    'order': 'desc'
                }
            }

        # Materialize the texts.

        result = config.es.search(

            index = cls.es_index,
            doc_type = cls.es_index,

            body = {
                'size': size,
                'sort': sort,
                'query': {
                    'bool': {
                        'must': conds
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


    @classmethod
    def get_text(cls, corpus, identifier):

        """
        Get an individual text document by corpus + identifier.

        Args:
            corpus (str)
            identifier (str)

        Returns: dict|None
        """

        result = config.es.search(

            index = cls.es_index,
            doc_type = cls.es_index,

            body = {
                'filter': {
                    'bool': {
                        'must': [
                            {'term': {
                                'corpus': corpus
                            }},
                            {'term': {
                                'identifier': identifier
                            }},
                        ]
                    }
                }
            }

        )

        if result['hits']['total'] > 0:
            return result['hits']['hits'][0]
