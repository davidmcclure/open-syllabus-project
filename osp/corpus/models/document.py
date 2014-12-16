

from osp.common.models.base import BaseModel
from peewee import *


class Document(BaseModel):


    path = CharField()
    stored_id = IntegerField()


    class Meta:
        db_name = 'document'
