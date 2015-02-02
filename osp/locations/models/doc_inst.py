

import datetime

from osp.common.models.base import LocalModel
from osp.institutions.models.institution import Institution
from peewee import *


class Document_Institution(LocalModel):

    created = DateTimeField(default=datetime.datetime.now)
    institution = ForeignKeyField(Institution)
    document = CharField()
