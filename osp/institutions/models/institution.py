

import datetime

from osp.common.models.base import BaseModel
from peewee import *
from playhouse.postgres_ext import *


class Institution(BaseModel):


    stored_id = BigIntegerField(null=True)
    metadata = HStoreField()


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
            return ' '.join([c_street, c_city, c_state, 'US'])

        # Or, institution address:
        i_street = self.metadata['Institution_Address']
        i_city   = self.metadata['Institution_City']
        i_state  = self.metadata['Institution_State']

        if i_street and i_city and i_state:
            return ' '.join([i_street, i_city, i_state, 'US'])
