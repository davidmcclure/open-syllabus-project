

from osp.common.config import config
from osp.citations.hlom.models.record import HLOM_Record
from elasticsearch.helpers import bulk
from playhouse.postgres_ext import ServerSide
from clint.textui.progress import bar


class HLOMIndex:


    def __init__(self):

        """
        Set the Elasticsearch connection.
        """

        self.es = config.get_es()


    def create(self):

        """
        Set the Elasticsearch mapping.
        """

        self.es.indices.create('hlom', {
            'mappings': {
                'record': {
                    '_id': {
                        'index': 'not_analyzed',
                        'store': True
                    },
                    'properties': {
                        'author': {
                            'type': 'string'
                        },
                        'title': {
                            'type': 'string'
                        },
                        'publisher': {
                            'type': 'string'
                        },
                        'pubyear': {
                            'type': 'string'
                        },
                        'count': {
                            'type': 'integer'
                        },
                        'rank': {
                            'type': 'integer'
                        },
                        'percent': {
                            'type': 'float'
                        }
                    }
                }
            }
        })


    def index(self):

        """
        Insert documents.
        """

        query = HLOM_Record.select_cited()
        count = query.count()
        print(count)

        def stream():
            for row in bar(ServerSide(query), expected_size=count):
                yield row.es_doc

        bulk( # Batch-insert the documents.
            self.es,
            stream(),
            raise_on_exception=False,
            index='hlom',
            doc_type='record'
        )

        # Commit the index.
        self.es.indices.flush('hlom')


    def delete(self):

        """
        Delete the index.
        """

        if self.es.indices.exists('hlom'):
            self.es.indices.delete('hlom')


    def count(self):

        """
        Count the number of documents.

        Returns:
            int: The number of docs.
        """

        return self.es.count('hlom', 'record')['count']


    def reset(self):

        """
        Clear and recreate the index.
        """

        self.delete()
        self.create()
