

import datetime

from osp.common.models.base import BaseModel
from peewee import *


class Format(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    format = CharField()


    class Meta:
        db_table = 'document_format'
