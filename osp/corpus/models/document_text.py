

from osp.common import config
from osp.common.models.base import BaseModel
from osp.corpus.models import Document

from peewee import ForeignKeyField, TextField


class Document_Text(BaseModel):


    document = ForeignKeyField(Document, unique=True)
    text = TextField()


    class Meta:
        database = config.get_table_db('document_text')
