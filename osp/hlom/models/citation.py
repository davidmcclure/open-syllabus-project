

import datetime

from osp.common.models.base import ServerModel
from peewee import *


class HLOM_Citation(ServerModel):

    document = CharField()
    record = CharField()
