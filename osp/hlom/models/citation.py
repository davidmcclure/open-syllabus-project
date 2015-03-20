

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.hlom.models.record import HLOM_Record
from osp.corpus.models.document import Document
from peewee import *


class HLOM_Citation(BaseModel):

    document = ForeignKeyField(Document)
    record = ForeignKeyField(HLOM_Record)

    class Meta:
        database = config.get_table_db('hlom_citation')
