

import csv
import pkgutil

from osp.common.config import config
from osp.common.models.base import BaseModel
from playhouse.postgres_ext import BinaryJSONField
from io import StringIO


class Institution(BaseModel):


    metadata = BinaryJSONField(default={})


    class Meta:
        database = config.get_table_db('institution')


    @classmethod
    def insert_institutions(cls):

        """
        Write institution rows into the database.
        """

        data = pkgutil.get_data(
            'osp.institutions',
            'data/institutions.csv'
        )

        reader = csv.DictReader(StringIO(data.decode('utf8')))

        rows = []
        for row in reader:
            rows.append({'metadata': row})

        with cls._meta.database.transaction():
            cls.insert_many(rows).execute()


    @property
    def geocoding_query(self):

        """
        Build a geolocation query.
        """

        # Campus address:
        c_street = self.metadata['Campus_Address']
        c_city   = self.metadata['Campus_City']
        c_state  = self.metadata['Campus_State']

        if c_street and c_city and c_state:
            return ','.join([c_street, c_city, c_state, 'USA'])

        # Or, institution address:
        i_street = self.metadata['Institution_Address']
        i_city   = self.metadata['Institution_City']
        i_state  = self.metadata['Institution_State']

        if i_street and i_city and i_state:
            return ','.join([i_street, i_city, i_state, 'USA'])
