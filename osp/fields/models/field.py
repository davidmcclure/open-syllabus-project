

import re

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.utils import read_csv
from osp.fields.utils import clean_field_name, parse_abbrs

from peewee import CharField, BooleanField
from playhouse.postgres_ext import ArrayField


class Field(BaseModel):


    primary_field = CharField(index=True, null=True)
    secondary_field = CharField(index=True, null=True)
    abbreviations = ArrayField(CharField, null=True)
    alpha_category = BooleanField(default=False)


    class Meta:
        database = config.get_table_db('field')


    @classmethod
    def insert_fields(cls):

        """
        Write field rows into the database.
        """

        reader = read_csv(
            'osp.fields',
            'data/fields.csv'
        )

        rows = []
        for row in reader:

            # Sanitize the field names.
            pf = clean_field_name(row['Primary Field'])
            sf = clean_field_name(row['Secondary Field'])

            # Parse the abbreviations.
            abbrs = parse_abbrs(row['ABBRV'])

            # Remove semantically-unfocused strings.
            abbrs = filter_abbrs(abbrs)

            alpha = bool(row['Alpha Category'])

            rows.append({
                'primary_field':    pf,
                'secondary_field':  sf,
                'abbreviations':    abbrs,
                'alpha_category':   alpha,
            })

        with cls._meta.database.transaction():
            cls.insert_many(rows).execute()


    def make_regex(self, pattern):

        """
        Produce regex queries.

        Args:
            pattern (str): The regex pattern.

        Returns: list
        """

        names = []

        # English + ENGLISH
        if self.secondary_field:
            names.append(self.secondary_field)
            names.append(self.secondary_field.upper())

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
