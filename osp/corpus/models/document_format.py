

import datetime

from osp.common.models.base import BaseModel
from peewee import *


class DocumentFormat(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    format = CharField()
