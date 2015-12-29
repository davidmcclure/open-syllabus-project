

import pkgutil

from osp.common.config import config
from osp.common.utils import read_csv, parse_domain
from osp.common.models.base import BaseModel

from peewee import CharField, IntegrityError
from bs4 import BeautifulSoup


class Institution(BaseModel):


    name = CharField()
    url = CharField(unique=True)
    domain = CharField(unique=True)
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

        for row in reader:
            if row['e_country'] == 'USA':

                # Normalize the URL.
                url = row['web_url'].strip()
                domain = parse_domain(url)

                # Clean the fields.
                name = row['biz_name'].strip()
                state = row['e_state'].strip()

                try:
                    cls.create(
                        name=name,
                        url=url,
                        domain=domain,
                        state=state,
                        country='US',
                    )

                except IntegrityError:
                    pass


    @classmethod
    def ingest_world(cls,
        package='osp.institutions',
        path='data/world.csv',
    ):

        """
        Insert world universities.
        """

        reader = read_csv(package, path)

        for row in reader:
            if row['country'] != 'US':

                # Normalize the URL.
                url = row['url'].strip()
                domain = parse_domain(url)

                # Clean the fields.
                name = row['name'].strip()
                country = row['country'].strip()

                try:
                    cls.create(
                        name=name,
                        url=url,
                        domain=domain,
                        state=None,
                        country=country,
                    )

                except IntegrityError:
                    pass
