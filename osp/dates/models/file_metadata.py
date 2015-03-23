

import time

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.corpus.models.document import Document
from peewee import *


class Document_Date_File_Metadata(BaseModel):


    class Meta:
        database = config.get_table_db('document_date_file_metadata')


    document = ForeignKeyField(Document, unique=True)
    date = DateTimeField()
