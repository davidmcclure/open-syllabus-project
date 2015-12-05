

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.utils import read_csv, query_bar
from playhouse.postgres_ext import BinaryJSONField
from peewee import fn


class Institution(BaseModel):


    metadata = BinaryJSONField(default={})


    class Meta:
        database = config.get_table_db('institution')


    @classmethod
    def insert_institutions(cls):

        """
        Write institution rows into the database.
        """

        reader = read_csv(
            'osp.institutions',
            'data/institutions.csv'
        )

        rows = []
        for row in reader:
            rows.append({'metadata': row})

        with cls._meta.database.transaction():
            cls.insert_many(rows).execute()
