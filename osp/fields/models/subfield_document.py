

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.fields.models import Subfield
from osp.corpus.models import Document
from peewee import ForeignKeyField, CharField


class Subfield_Document(BaseModel):


    subfield = ForeignKeyField(Subfield)
    document = ForeignKeyField(Document)
    snippet = CharField()


    class Meta:
        database = config.get_table_db('subfield_document')
