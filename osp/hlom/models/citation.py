

import datetime

from osp.common.models.base import BaseModel
from peewee import *


class HLOM_Citation(BaseModel):

    document = CharField()
    record = CharField()
