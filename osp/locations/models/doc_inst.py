

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.institutions.models.institution import Institution
from osp.corpus.models.document import Document
from peewee import *


class Document_Institution(BaseModel):

    document = ForeignKeyField(Document)
    institution = ForeignKeyField(Institution)

    class Meta:
        database = config.get_table_db('document_institution')
