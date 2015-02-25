

import datetime

from osp.common.models.base import RemoteModel
from osp.citations.hlom.models.record import HLOM_Record
from osp.corpus.models.document import Document
from peewee import *


class HLOM_Citation(RemoteModel):

    document = ForeignKeyField(Document)
    record = ForeignKeyField(HLOM_Record)
