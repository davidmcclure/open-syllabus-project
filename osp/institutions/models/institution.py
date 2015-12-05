

import pkgutil

from osp.common.config import config
from osp.common.utils import read_csv, parse_domain
from osp.common.models.base import BaseModel

from peewee import CharField, IntegrityError
from bs4 import BeautifulSoup


class Institution(BaseModel):


    name = CharField()
    domain = CharField(unique=True)


    class Meta:
        database = config.get_table_db('institution')


    @classmethod
    def insert_us(cls):

        """
        Insert US institutions.
        """

        html = pkgutil.get_data(
            'osp.institutions',
            'data/us.html',
        )

        root = BeautifulSoup(html.decode('utf8'), 'html.parser')

        for link in root.select('li a'):

            # Clean the values.
            name = link.get_text().strip()
            domain = parse_domain(link.attrs['href'])

            # Write the row.
            try: cls.create(name=name, domain=domain)
            except IntegrityError: pass


    @classmethod
    def insert_uk(cls):

        """
        Insert UK institutions.
        """

        reader = read_csv(
            'osp.institutions',
            'data/uk.csv',
        )

        for row in reader:

            # Clean the values.
            name = row['name'].strip()
            domain = parse_domain(row['url'])

            # Write the row.
            try: cls.create(name=name, domain=domain)
            except IntegrityError: pass
