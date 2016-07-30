

from peewee import ForeignKeyField

from osp.common import config
from osp.common.models.base import BaseModel
from osp.institutions.models import Institution
from osp.corpus.models import Document


class Institution_Document(BaseModel):


    institution = ForeignKeyField(Institution)
    document = ForeignKeyField(Document)


    class Meta:
        database = config.get_table_db('institution_document')
