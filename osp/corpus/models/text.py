

import datetime

from osp.corpus.models.document import Document
from peewee import *


class Document_Text(Model):

    created = DateTimeField(default=datetime.datetime.now)
    document = ForeignKeyField(Document)
    text = TextField()

    class Meta:
        database = config.get_db('document_text')
