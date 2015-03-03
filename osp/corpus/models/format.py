

import datetime

from osp.common.config import config
from osp.corpus.models.document import Document
from peewee import *


class Document_Format(Model):

    created = DateTimeField(default=datetime.datetime.now)
    document = ForeignKeyField(Document)
    format = CharField(index=True)

    class Meta:
        database = config.get_db('document_format')
