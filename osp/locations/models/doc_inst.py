

import datetime

from osp.common.models.base import ServerModel
from osp.institutions.models.institution import Institution
from peewee import *


class Document_Institution(ServerModel):

    created = DateTimeField(default=datetime.datetime.now)
    institution = ForeignKeyField(Institution)
    document = CharField()
