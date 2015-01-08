

import datetime

from osp.common.models.base import BaseModel
from peewee import *


class Document_Format(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    format = CharField()
