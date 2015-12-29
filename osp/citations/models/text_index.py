

from osp.common.config import config
from osp.common.utils import query_bar
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.citations.models import Text
from osp.citations.data.corpora import CORPORA


class Text_Index(Elasticsearch):


    es_index = 'text'


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

        for row in query_bar(Text.select()):

            yield dict(
                _id         = row.id,
                title       = row.title,
                author      = row.author,
                publisher   = row.publisher,
                date        = row.date,
                journal     = row.journal_title,
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
                        'author',
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

        facets = []
        for slug, count in counts:

            facets.append(dict(
                label=CORPORA.get(slug),
                value=slug,
                count=count,
            ))

        return facets
