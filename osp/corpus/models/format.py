

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.corpus.models.document import Document
from peewee import *


class Document_Format(BaseModel):

    document = ForeignKeyField(Document, unique=True)
    format = CharField(index=True)

    class Meta:
        database = config.get_table_db('document_format')
