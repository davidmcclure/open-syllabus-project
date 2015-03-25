

from osp.common.config import config
from osp.corpus.models.text import Document_Text
from elasticsearch.helpers import bulk
from playhouse.postgres_ext import ServerSide


class CorpusIndex:


    def create(self):

        """
        Set the Elasticsearch mapping.
        """

        config.es.indices.create('osp', {
            'mappings': {
                'syllabus': {
                    '_id': {
                        'index': 'not_analyzed',
                        'store': True
                    },
                    'properties': {
                        'doc_id': {
                            'type': 'integer'
                        },
                        'body': {
                            'type': 'string'
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
            for row in ServerSide(Document_Text.select()):
                yield row.es_doc

        bulk( # Batch-insert the documents.
            config.es,
            stream(),
            raise_on_exception=False,
            index='osp',
            doc_type='syllabus'
        )

        # Commit the index.
        config.es.indices.flush('osp')


    def delete(self):

        """
        Delete the index.
        """

        if config.es.indices.exists('osp'):
            config.es.indices.delete('osp')


    def count(self):

        """
        Count the number of documents.

        Returns:
            int: The number of docs.
        """

        return config.es.count('osp', 'syllabus')['count']


    def reset(self):

        """
        Clear and recreate the index.
        """

        self.delete()
        self.create()
