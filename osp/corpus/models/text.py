

import datetime

from osp.common.models.base import LocalModel
from osp.corpus.models.document import Document
from peewee import *


class Document_Text(LocalModel):

    created = DateTimeField(default=datetime.datetime.now)
    document = ForeignKeyField(Document)
    text = TextField()
