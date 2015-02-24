

import datetime

from osp.common.models.base import LocalModel
from peewee import *


class Document_Text(LocalModel):

    created = DateTimeField(default=datetime.datetime.now)
    document = CharField(index=True)
    text = TextField()
