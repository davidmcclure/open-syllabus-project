

import datetime

from osp.common.models.base import BaseModel
from peewee import *


class Document_Text(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    text = TextField()
