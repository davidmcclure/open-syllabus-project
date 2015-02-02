

import datetime

from osp.common.models.base import WorkerModel
from peewee import *


class Document_Text(WorkerModel):

    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    text = TextField()
