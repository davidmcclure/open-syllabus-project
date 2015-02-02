

from osp.common.models.base import LocalModel
from peewee import *
from playhouse.postgres_ext import *


class HLOM_Record(LocalModel):

    control_number = CharField(unique=True)
    record = BlobField()
