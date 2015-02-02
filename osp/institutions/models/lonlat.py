

import datetime

from osp.common.models.base import WorkerModel
from osp.institutions.models.institution import Institution
from peewee import *


class Institution_LonLat(WorkerModel):

    created = DateTimeField(default=datetime.datetime.now)
    institution = ForeignKeyField(Institution)
    lon = DecimalField()
    lat = DecimalField()
