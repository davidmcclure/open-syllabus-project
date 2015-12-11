

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.models import Text
from osp.corpus.models import Document

from peewee import ForeignKeyField, FloatField


class Citation(BaseModel):


    text = ForeignKeyField(Text)
    document = ForeignKeyField(Document)
    min_freq = FloatField()


    class Meta:
        database = config.get_table_db('citation')
        indexes = ((('document', 'text'), True),)
