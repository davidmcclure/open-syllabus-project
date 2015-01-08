

import datetime

from osp.common.models.base import BaseModel
from peewee import *


class DocumentText(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    text = TextField()
