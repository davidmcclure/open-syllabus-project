

import datetime

from osp.common.models.base import RemoteModel
from osp.institutions.models.institution import Institution
from osp.corpus.models.document import Document
from peewee import *


class Document_Institution(RemoteModel):

    created = DateTimeField(default=datetime.datetime.now)
    document = ForeignKeyField(Document)
    institution = ForeignKeyField(Institution)
