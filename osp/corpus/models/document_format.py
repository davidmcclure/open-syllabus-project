

from osp.common import config
from osp.common.models import BaseModel
from osp.corpus.models import Document

from peewee import ForeignKeyField, CharField, fn


class Document_Format(BaseModel):


    document = ForeignKeyField(Document, unique=True)
    format = CharField(index=True)


    class Meta:
        database = config.get_table_db('document_format')


    @classmethod
    def format_counts(cls):

        """
        Map unique file formats to document counts.
        """

        count = fn.Count(cls.id)

        query = (
            cls
            .select(cls.format, count.alias('count'))
            .distinct(cls.document)
            .group_by(cls.format)
            .order_by(count.desc())
        )

        counts = []
        for c in query.iterator():
            counts.append((c.format, c.count))

        return counts
