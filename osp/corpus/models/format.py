

import datetime

from osp.common.models.base import LocalModel
from osp.corpus.models.document import Document
from peewee import *


class Document_Format(LocalModel):

    created = DateTimeField(default=datetime.datetime.now)
    document = ForeignKeyField(Document)
    format = CharField(index=True)
