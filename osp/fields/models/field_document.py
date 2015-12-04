

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.fields.models.field import Field
from osp.corpus.models.document import Document
from peewee import ForeignKeyField, CharField


class Field_Document(BaseModel):


    field = ForeignKeyField(Field)
    document = ForeignKeyField(Document)
    snippet = CharField()


    class Meta:
        database = config.get_table_db('field_document')
