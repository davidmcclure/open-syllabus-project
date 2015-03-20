

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.corpus.models.document import Document
from elasticsearch.helpers import bulk
from playhouse.postgres_ext import ServerSide
from peewee import *


class Document_Text(BaseModel):


    document = ForeignKeyField(Document, unique=True)
    text = TextField()


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


    class Meta:
        database = config.get_table_db('document_text')
