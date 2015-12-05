

from osp.common.config import config
from osp.common.utils import read_csv, parse_domain
from osp.common.models.base import BaseModel

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

            # Extract the domain name.
            website = parse_domain(row['Institution_Web_Address'])

            query = cls.select().where(
                cls.name==name,
                cls.website==website,
            )

            if name and website and not query.exists():
                cls.create(name=name, website=website)
