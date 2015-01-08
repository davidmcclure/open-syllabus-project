

import datetime

from osp.common.models.base import BaseModel
from osp.institutions.models.institution import Institution
from peewee import *


class Document_Institution(BaseModel):


    created = DateTimeField(default=datetime.datetime.now)
    institution = ForeignKeyField(Institution)
    document = CharField()
