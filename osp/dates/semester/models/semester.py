

import datetime

from osp.common.models.base import WorkerModel
from peewee import *


class Document_Semester(WorkerModel):

    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    offset = IntegerField()
    year = IntegerField()
    semester = CharField()
