

import datetime

from osp.common.models.base import LocalModel
from osp.institutions.models.institution import Institution
from peewee import *


class Institution_LonLat(LocalModel):

    created = DateTimeField(default=datetime.datetime.now)
    institution = ForeignKeyField(Institution)
    lon = DecimalField()
    lat = DecimalField()
