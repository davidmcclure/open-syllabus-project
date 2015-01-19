

import datetime

from osp.common.models.base import BaseModel
from peewee import *
from playhouse.postgres_ext import *


class HLBD_Record(BaseModel):

    control_number = CharField()
    metadata = HStoreField()
