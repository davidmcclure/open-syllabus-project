

import datetime

from osp.common.models.base import BaseModel
from peewee import *


class Text(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    text = TextField()


    class Meta:
        db_table = 'document_text'
