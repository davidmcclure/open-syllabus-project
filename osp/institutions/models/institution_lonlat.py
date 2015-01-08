

import datetime

from osp.common.models.base import BaseModel
from osp.institutions.models.institution import Institution
from peewee import *


class Institution_LonLat(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    institution = ForeignKeyField(Institution)
    lon = DecimalField()
    lat = DecimalField()
