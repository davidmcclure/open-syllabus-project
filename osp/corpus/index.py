

from osp.common.config import config
from osp.corpus.models.text import Document_Text
from elasticsearch.helpers import bulk
from playhouse.postgres_ext import ServerSide
from clint.textui.progress import bar


class CorpusIndex:


    def __init__(self):

        """
        Set the Elasticsearch connection.
        """

        self.es = config.get_es()


    def create(self):

        """
        Set the Elasticsearch mapping.
        """

        self.es.indices.create('osp', {
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

        query = Document_Text.select()
        count = query.count()

        def stream():
            for row in bar(ServerSide(query), expected_size=count):
                yield row.es_doc

        bulk( # Batch-insert the documents.
            self.es,
            stream(),
            raise_on_exception=False,
            index='osp',
            doc_type='syllabus'
        )

        # Commit the index.
        self.es.indices.flush('osp')


    def delete(self):

        """
        Delete the index.
        """

        if self.es.indices.exists('osp'):
            self.es.indices.delete('osp')


    def count(self):

        """
        Count the number of documents.

        Returns:
            int: The number of docs.
        """

        return self.es.count('osp', 'syllabus')['count']


    def reset(self):

        """
        Clear and recreate the index.
        """

        self.delete()
        self.create()
