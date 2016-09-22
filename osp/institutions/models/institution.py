

import pkgutil

from peewee import CharField
from bs4 import BeautifulSoup

from osp.common import config
from osp.common.utils import read_csv, parse_domain
from osp.common.models import BaseModel
from osp.institutions.utils import strip_csv_row


class Institution(BaseModel):

    name = CharField()
    url = CharField(unique=True)
    state = CharField(null=True)
    country = CharField()

    class Meta:
        database = config.get_table_db('institution')

    @classmethod
    def ingest_usa(cls,
        package='osp.institutions',
        path='data/usa.csv',
    ):

        """
        Insert US universities.
        """

        reader = read_csv(package, path)

        for row in map(strip_csv_row, reader):
            if row['e_country'] == 'USA':

                try:
                    cls.create(
                        name=row['biz_name'],
                        url=row['web_url'],
                        state=row['e_state'],
                        country='US',
                    )

                except Exception as e:
                    print(e)

    @classmethod
    def ingest_world(cls,
        package='osp.institutions',
        path='data/world.csv',
    ):

        """
        Insert world universities.
        """

        reader = read_csv(package, path)

        for row in map(strip_csv_row, reader):
            if row['country'] != 'US':

                try:
                    cls.create(
                        name=row['name'],
                        url=row['url'],
                        country=row['country'],
                    )

                except Exception as e:
                    print(e)
