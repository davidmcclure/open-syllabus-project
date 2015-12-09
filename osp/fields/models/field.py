

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.utils import read_csv
from osp.fields.utils import clean_field_name

from peewee import CharField


class Field(BaseModel):


    name = CharField(index=True)


    class Meta:
        database = config.get_table_db('field')
