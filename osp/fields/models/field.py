

from osp.common import config
from osp.common.models.base import BaseModel

from peewee import CharField


class Field(BaseModel):


    name = CharField(index=True)


    class Meta:
        database = config.get_table_db('field')
