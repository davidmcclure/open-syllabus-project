

import datetime

from osp.common.models.base import BaseModel
from osp.institutions.models.institution import Institution
from peewee import *


class LonLat(BaseModel):


    created     = DateTimeField(default=datetime.datetime.now)
    institution = ForeignKeyField(Institution, related_name='lonlats')
    lon         = DecimalField()
    lat         = DecimalField()


    class Meta:
        db_table = 'institution_lonlat'
