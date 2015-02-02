

import datetime

from osp.common.models.base import LocalModel
from peewee import *


class Document_Semester(LocalModel):

    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    offset = IntegerField()
    year = IntegerField()
    semester = CharField()
