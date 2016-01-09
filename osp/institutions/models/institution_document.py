

from osp.common import config
from osp.common.models.base import BaseModel
from osp.institutions.models import Institution
from osp.corpus.models import Document

from peewee import ForeignKeyField


class Institution_Document(BaseModel):


    institution = ForeignKeyField(Institution)
    document = ForeignKeyField(Document)


    class Meta:
        database = config.get_table_db('institution_document')
