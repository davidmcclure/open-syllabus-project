

import datetime

from osp.common.models.base import BaseModel
from peewee import *


class Date(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    date = DateField()
    generation = CharField()


    class Meta:
        db_table = 'document_date'
