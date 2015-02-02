

from osp.common.models.base import WorkerModel
from peewee import *
from playhouse.postgres_ext import *


class HLOM_Record(WorkerModel):

    control_number = CharField(unique=True)
    record = BlobField()
