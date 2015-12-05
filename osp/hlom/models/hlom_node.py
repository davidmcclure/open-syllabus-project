

from osp.common.config import config
from osp.common.models.base import BaseModel
from playhouse.postgres_ext import *
from peewee import *


class HLOM_Node(BaseModel):


    control_number = CharField(unique=True, null=False)
    node = BinaryJSONField(default={})


    class Meta:
        database = config.get_table_db('hlom_node')
