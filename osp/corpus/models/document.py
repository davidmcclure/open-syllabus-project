

from playhouse.postgres_ext import *
from osp.common.models.base import BaseModel
from peewee import *


class Document(BaseModel):


    stored_id = BigIntegerField(null=True)
    path = CharField(unique=True)


    class Meta:
        db_name = 'document'
