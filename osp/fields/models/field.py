

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.utils import read_csv

from peewee import CharField, BooleanField
from playhouse.postgres_ext import ArrayField


class Field(BaseModel):


    primary_field = CharField(index=True)
    secondary_field = CharField(index=True)
    abbreviations = ArrayField(CharField)
    alpha_category = BooleanField()


    class Meta:
        database = config.get_table_db('field')


    @classmethod
    def insert_fields(cls):

        """
        Write field rows into the database.
        """

        reader = read_csv(
            'osp.fields',
            'data/fields.csv'
        )

        for row in reader:
            print(row)
