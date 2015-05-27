

import re

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.corpus.models.document import Document
from playhouse.postgres_ext import TSVectorField
from peewee import *


class Document_Search(BaseModel):


    document = ForeignKeyField(Document, unique=True)
    text = TSVectorField()


    class Meta:
        database = config.get_table_db('document_search')
