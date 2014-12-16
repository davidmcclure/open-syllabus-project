

import datetime

from playhouse.postgres_ext import *
from osp.common.models.base import BaseModel
from peewee import *


class Institution(BaseModel):


    metadata = HStoreField()
    stored_id = BigIntegerField(null=True)


    @classmethod
    def join_lonlats(cls):

        """
        Join on the most recent lon/lats.
        """

        from osp.institutions.models.lonlat import LonLat

        return (
            cls
            .select(cls, LonLat.lon, LonLat.lat)
            .distinct([cls.id])
            .join(LonLat, JOIN_LEFT_OUTER)
            .order_by(cls.id, LonLat.created.desc())
        )


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
            return ' '.join([c_street, c_city, c_state])

        # Or, institution address:
        i_street = self.metadata['Institution_Address']
        i_city   = self.metadata['Institution_City']
        i_state  = self.metadata['Institution_State']

        if i_street and i_city and i_state:
            return ' '.join([i_street, i_city, i_state])


    class Meta:
        db_name = 'institution'
