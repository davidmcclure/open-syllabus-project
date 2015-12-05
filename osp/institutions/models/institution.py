

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.utils import read_csv

from peewee import CharField


class Institution(BaseModel):


    name = CharField()
    website = CharField()


    class Meta:
        database = config.get_table_db('institution')


    @classmethod
    def insert_us(cls):

        """
        Write institution rows into the database.
        """

        reader = read_csv(
            'osp.institutions',
            'data/us-inst.csv',
        )

        rows = []
        for row in reader:
            pass # TODO

        with cls._meta.database.transaction():
            cls.insert_many(rows).execute()
