

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.models import Text
from osp.corpus.models import Document
from playhouse.postgres_ext import *
from peewee import *


class Citation(BaseModel):


    document = ForeignKeyField(Document)
    text = ForeignKeyField(Text)


    class Meta:
        database = config.get_table_db('citation')
        indexes = ((('document', 'text'), True),)
