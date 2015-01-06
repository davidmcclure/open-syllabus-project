

import datetime

from osp.common.models.base import BaseModel
from peewee import *


class FileFormat(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    document = CharField()
    file_format = CharField()


    class Meta:
        db_table = 'document_file_format'
