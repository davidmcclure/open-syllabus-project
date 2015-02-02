

from playhouse.postgres_ext import *
from osp.common.models.base import WorkerModel
from peewee import *


class Document(WorkerModel):

    stored_id = BigIntegerField(null=True)
    path = CharField(unique=True)
