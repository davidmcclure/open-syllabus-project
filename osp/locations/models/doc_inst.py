

import datetime

from osp.common.models.base import BaseModel
from osp.institutions.models.institution import Institution
from peewee import *


class DocInst(BaseModel):


    created     = DateTimeField(default=datetime.datetime.now)
    institution = ForeignKeyField(Institution)
    document    = CharField()


    class Meta:
        db_table = 'document_institution'
