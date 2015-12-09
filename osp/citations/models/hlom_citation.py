

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.models import Text
from osp.corpus.models import Document
from playhouse.postgres_ext import *
from peewee import *


class HLOM_Citation(BaseModel):


    document = ForeignKeyField(Document)
    record = ForeignKeyField(Text)


    class Meta:
        database = config.get_table_db('hlom_citation')
        indexes = ((('document', 'record'), True),)
