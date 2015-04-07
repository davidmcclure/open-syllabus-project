

from osp.common.config import config
from osp.common.models.elasticsearch import ElasticsearchModel
from osp.corpus.models.document import Document
from peewee import *


class Document_Text(ElasticsearchModel):


    document = ForeignKeyField(Document, unique=True)
    text = TextField()


    class Meta:
        database = config.get_table_db('document_text')


    es_index = 'osp'
    es_doc_type = 'syllabus'


    es_mapping = {
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


    @classmethod
    def es_query(cls):

        """
        Select rows that should be indexed in Elasticsearch.

        Returns:
            peewee.SelectQuery
        """

        return cls.select()


    @property
    def es_doc(self):

        """
        Construct a document for Elasticsearch.

        Returns:
            dict: The document fields.
        """

        return {
            '_id':      self.document.path,
            'doc_id':   self.document.id,
            'body':     self.text
        }
