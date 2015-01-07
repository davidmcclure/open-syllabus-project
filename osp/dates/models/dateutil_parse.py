

import datetime

from osp.common.models.base import BaseModel
from peewee import *


class DateutilParse(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    date = DateField()
    depth = IntegerField()


    class Meta:
        db_table = 'document_date_dateutil_parse'
