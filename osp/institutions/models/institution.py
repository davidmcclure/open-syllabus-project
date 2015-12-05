

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
        Write institution rows into the database.
        """

        html = pkgutil.get_data(
            'osp.institutions',
            'data/us-inst.html'
        )

        root = BeautifulSoup(html.decode('utf8'), 'html.parser')

        for link in root.select('li a'):

            # Clean the name.
            name = link.get_text().strip()

            # Normalize the domain.
            domain = parse_domain(link.attrs['href'])

            # Write the row.
            try: cls.create(name=name, domain=domain)
            except IntegrityError: pass
