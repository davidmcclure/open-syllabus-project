

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.corpus.models.document import Document
from peewee import *


class Document_Stored_Id(BaseModel):

    document = ForeignKeyField(Document, unique=True)
    stored_id = BigIntegerField(null=True)

    class Meta:
        database = config.get_db('document_stored_id')
