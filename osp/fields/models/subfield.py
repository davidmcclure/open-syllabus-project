

import re

from osp.common import config
from osp.common.models.base import BaseModel
from osp.common.utils import read_csv
from osp.fields.utils import clean_field_name, parse_abbrs, filter_abbrs
from osp.fields.models import Field

from peewee import CharField, BooleanField, ForeignKeyField
from playhouse.postgres_ext import ArrayField


class Subfield(BaseModel):


    name = CharField(index=True)
    abbreviations = ArrayField(CharField, null=True)
    field = ForeignKeyField(Field)


    class Meta:
        database = config.build_table_db('subfield')


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

            # Sanifize field names.
            pf = clean_field_name(row['Primary Field'])
            sf = clean_field_name(row['Secondary Field'])

            # Parse abbreviations.
            abbrs = parse_abbrs(row['ABBRV'])
            if abbrs: abbrs = filter_abbrs(abbrs)

            # If parent field, write row.
            if bool(row['Alpha Category']):
                Field.create(name=pf)

            # Query for a parent field.
            field = Field.select().where(Field.name==pf).first()

            if field:

                Subfield.create(
                    name=sf,
                    abbreviations=abbrs,
                    field=field,
                )


    def make_regex(self, pattern):

        """
        Produce regex queries.

        Args:
            pattern (str): The regex pattern.

        Returns: list
        """

        names = []

        # English + ENGLISH
        if self.name:
            names.append(self.name)
            names.append(self.name.upper())

        if self.abbreviations:
            names += self.abbreviations

        # Join names to (A|B|C...)
        names = '({:s})'.format('|'.join(names))

        return pattern.format(names)


    def search(self, text):

        """
        Find the first field code match in a string.

        Args:
            text (str): The subject text.

        Returns: SRE_Match
        """

        regex = self.make_regex('(^|\s){:s}[\s-]+[0-9]{{2,4}}')

        return re.search(regex, text)
