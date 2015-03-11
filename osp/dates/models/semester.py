

import time

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.corpus.models.document import Document
from peewee import *


class Document_Date_Semester(BaseModel):


    document = ForeignKeyField(Document, unique=True)
    date = DateTimeField()
    offset = IntegerField()


    class Meta:
        database = config.get_table_db('document_date_semester')
