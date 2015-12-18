

import pkgutil

from osp.common.config import config
from osp.common.utils import read_csv, parse_domain
from osp.common.models.base import BaseModel

from peewee import CharField, IntegrityError
from bs4 import BeautifulSoup


class Institution(BaseModel):


    name = CharField()
    domain = CharField(unique=True)
    state = CharField(null=True)
    country = CharField()


    class Meta:
        database = config.get_table_db('institution')


    @classmethod
    def ingest_usa(cls, package='osp.institutions', path='data/usa.csv'):

        """
        Insert US universities.
        """

        reader = read_csv(package, path)

        for row in reader:
            if row['e_country'] == 'USA':

                name = row['biz_name']
                domain = parse_domain(row['web_url'])
                state = row['e_state']

                try:
                    cls.create(
                        name=name,
                        domain=domain,
                        state=state,
                        country='US',
                    )

                except IntegrityError:
                    pass


    @classmethod
    def ingest_world(cls):

        """
        Insert world universities.
        """

        reader = read_csv(
            'osp.institutions',
            'data/world.csv',
        )

        for row in reader:
            if row['country'] != 'US':

                name = row['name']
                domain = parse_domain(row['url'])
                country = row['country']

                try:
                    cls.create(
                        name=name,
                        domain=domain,
                        country=country,
                    )

                except IntegrityError:
                    pass
