

from osp.common.config import config
from osp.common.utils import read_csv, parse_domain
from osp.common.models.base import BaseModel

from peewee import CharField


class Institution(BaseModel):


    name = CharField()
    domain = CharField(unique=True)


    class Meta:
        database = config.get_table_db('institution')


    @classmethod
    def insert_us(cls):

        """
        Write institution rows into the database.
        """

        pass
