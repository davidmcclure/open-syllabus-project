

from playhouse.postgres_ext import *
from osp.common.models.base import LocalModel
from peewee import *


class Document(LocalModel):

    stored_id = BigIntegerField(null=True)
    path = CharField(unique=True)
