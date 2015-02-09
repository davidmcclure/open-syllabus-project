

import datetime

from osp.common.models.base import RemoteModel
from peewee import *


class HLOM_Citation(RemoteModel):

    document = CharField()
    record = CharField()
