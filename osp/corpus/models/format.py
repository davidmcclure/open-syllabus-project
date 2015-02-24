

import datetime

from osp.common.models.base import LocalModel
from peewee import *


class Document_Format(LocalModel):

    created = DateTimeField(default=datetime.datetime.now)
    document = CharField(index=True)
    format = CharField()
