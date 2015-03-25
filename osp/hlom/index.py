

from osp.common.config import config
from osp.citations.hlom.models.record import HLOM_Record
from elasticsearch.helpers import bulk
from playhouse.postgres_ext import ServerSide


class HLOMIndex:


    def create(self):

        """
        Set the Elasticsearch mapping.
        """

        config.es.indices.create('hlom', {
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

        def stream():
            for row in ServerSide(HLOM_Record.select_cited()):
                yield row.es_doc

        bulk( # Batch-insert the documents.
            config.es,
            stream(),
            raise_on_exception=False,
            index='hlom',
            doc_type='record'
        )

        # Commit the index.
        config.es.indices.flush('hlom')


    def delete(self):

        """
        Delete the index.
        """

        if config.es.indices.exists('hlom'):
            config.es.indices.delete('hlom')


    def count(self):

        """
        Count the number of documents.

        Returns:
            int: The number of docs.
        """

        return config.es.count('hlom', 'record')['count']


    def reset(self):

        """
        Clear and recreate the index.
        """

        self.delete()
        self.create()
