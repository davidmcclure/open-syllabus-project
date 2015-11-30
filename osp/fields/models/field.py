

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.utils import read_csv
from osp.fields.utils import clean_field_name, parse_abbrs

from peewee import CharField, BooleanField
from playhouse.postgres_ext import ArrayField


class Field(BaseModel):


    primary_field = CharField(index=True)
    secondary_field = CharField(index=True)
    abbreviations = ArrayField(CharField)
    alpha_category = BooleanField()


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

            # Split the abbreviations.
            abbrs = parse_abbrs(row['ABBRV'])
            alpha = bool(row['Alpha Category'])

            rows.append({
                'primary_field':    pf,
                'secondary_field':  sf,
                'abbreviations':    abbrs,
                'alpha_category':   alpha,
            })

        with cls._meta.database.transaction():
            cls.insert_many(rows).execute()


    def query_regexes(self, pattern='{:s}\s+[0-9]{{2,4}}'):

        """
        Produce regex queries.

        Args:
            pattern (str): The regex pattern.

        Returns: list
        """

        names = [self.secondary_field] + self.abbreviations

        queries = []
        for n in names:
            queries.append(pattern.format(n))

        return queries
