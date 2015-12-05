

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.utils import read_csv

from peewee import CharField


class Institution(BaseModel):


    name = CharField()
    website = CharField()


    class Meta:

        database = config.get_table_db('institution')

        indexes = (
            (('name', 'website'), True),
        )


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

            name = row['Institution_Name'].strip()
            website = row['Institution_Web_Address'].strip()

            query = cls.select().where(
                cls.name==name,
                cls.website==website,
            )

            if name and website and not query.exists():
                cls.create(name=name, website=website)
