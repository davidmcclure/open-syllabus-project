

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.corpus.models.document import Document
from elasticsearch.helpers import bulk
from playhouse.postgres_ext import ServerSide
from peewee import *


class Document_Text(BaseModel):


    document = ForeignKeyField(Document, unique=True)
    text = TextField()


    @classmethod
    def es_create(cls):

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
                        'body': {
                            'type': 'string'
                        }
                    }
                }
            }
        })


    @classmethod
    def es_delete(cls):

        """
        Delete the Elasticsearch index.
        """

        if config.es.indices.exists('osp'):
            config.es.indices.delete('osp')


    @classmethod
    def es_count(cls):

        """
        Count the number of docs in Elasticsearch.

        Returns:
            int: The number of docs.
        """

        return config.es.count('osp', 'syllabus')['count']


    @classmethod
    def es_index(cls):

        """
        Insert documents into Elasticsearch.
        """

        def stream():
            for row in ServerSide(cls.select()):
                yield row.es_doc

        # Batch-insert the documents.
        bulk(config.es, stream(), index='osp', doc_type='syllabus')


    @property
    def es_doc(self):

        """
        Construct a document for Elasticsearch.

        Returns:
            dict: The document fields.
        """

        return {
            '_id': self.document.path,
            'body': self.text
        }


    class Meta:
        database = config.get_table_db('document_text')
