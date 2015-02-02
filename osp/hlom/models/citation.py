

import datetime

from osp.common.models.base import LocalModel
from peewee import *


class HLOM_Citation(LocalModel):

    document = CharField()
    record = CharField()
