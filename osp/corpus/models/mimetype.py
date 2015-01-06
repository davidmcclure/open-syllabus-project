

import datetime

from osp.common.models.base import BaseModel
from osp.corpus.models.document import Document
from peewee import *


class Mimetype(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    document = ForeignKeyField(Document)
    mime_type = CharField()


    class Meta:
        db_table = 'document_mimetype'
