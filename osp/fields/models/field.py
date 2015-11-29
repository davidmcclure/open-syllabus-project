

from osp.common.config import config
from osp.common.models.base import BaseModel

from peewee import CharField
from playhouse.postgres_ext import ArrayField


class Field(BaseModel):


    primary_field = CharField(index=True)
    secondary_field = CharField(index=True)
    abbreviations = ArrayField(CharField)


    class Meta:
        database = config.get_table_db('field')
