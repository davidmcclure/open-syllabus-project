

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.hlom.models.node import HLOM_Node
from peewee import *


class HLOM_Edge(BaseModel):


    source = ForeignKeyField(HLOM_Node, related_name='sources')
    target = ForeignKeyField(HLOM_Node, related_name='targets')
    weight = IntegerField(index=True)


    class Meta:
        database = config.get_table_db('hlom_edge')
