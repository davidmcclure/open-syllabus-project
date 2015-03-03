

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.corpus.models.document import Document
from peewee import *


class Document_Text(BaseModel):

    document = ForeignKeyField(Document, unique=True)
    text = TextField()

    class Meta:
        database = config.get_table_db('document_text')
