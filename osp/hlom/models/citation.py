

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.hlom.models.record import HLOM_Record
from osp.corpus.models.document import Document
from playhouse.postgres_ext import *
from peewee import *


class HLOM_Citation(BaseModel):


    document = ForeignKeyField(Document)
    record = ForeignKeyField(HLOM_Record)


    class Meta:
        database = config.get_table_db('hlom_citation')
        indexes = ((('document', 'record'), True),)
