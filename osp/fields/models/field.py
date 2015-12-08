

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.utils import read_csv
from osp.fields.utils import clean_field_name

from peewee import CharField


class Field(BaseModel):


    name = CharField(index=True)


    class Meta:
        database = config.get_table_db('field')


    @classmethod
    def ingest(cls, package='osp.fields', path='data/fields.csv'):

        """
        Ingest fields.

        Args:
            package (str)
            path (str)
        """

        reader = read_csv(package, path)

        for row in reader:
            cls.create(name=clean_field_name(row['Primary Field']))
