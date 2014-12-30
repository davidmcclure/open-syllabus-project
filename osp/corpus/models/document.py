

from playhouse.postgres_ext import *
from osp.common.models.base import BaseModel
from peewee import *


class Document(BaseModel):


    path = CharField(unique=True)
    stored_id = BigIntegerField(null=True)
    metadata = HStoreField(null=True)


    class Meta:
        db_name = 'document'
