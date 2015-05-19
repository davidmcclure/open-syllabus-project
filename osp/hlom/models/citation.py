

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.hlom.models.record import HLOM_Record
from osp.corpus.models.document import Document
from peewee import *


class HLOM_Citation(BaseModel):


    document = ForeignKeyField(Document)
    record = ForeignKeyField(HLOM_Record)
    metadata = BinaryJSONField(default={})


    class Meta:
        database = config.get_table_db('hlom_citation')
        indexes = ((('document', 'record'), True),)


    @classmethod
    def text_counts(cls):

        """
        Get an ordered list of HLOM record -> citation counts.
        """

        count = fn.Count(cls.id)

        return (
            cls
            .select(cls.record, count.alias('count'))
            .group_by(cls.record)
            .distinct(cls.record)
            .order_by(count.desc())
        )
