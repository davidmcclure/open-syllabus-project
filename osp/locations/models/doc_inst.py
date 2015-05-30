

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.institutions.models.institution import Institution
from osp.corpus.models.document import Document
from peewee import *


class Document_Institution(BaseModel):


    document = ForeignKeyField(Document, unique=True)
    institution = ForeignKeyField(Institution)


    class Meta:
        database = config.get_table_db('document_institution')


    @classmethod
    def institution_counts(cls):

        """
        Map institution ids to syllabus counts.

        Returns:
            dict: id -> count.
        """

        count = fn.COUNT(cls.document)

        query = (
            cls.select(cls.institution, count)
            .distinct([cls.institution])
            .group_by(cls.institution)
        )

        print(query.sql())

        counts = {}
        for row in query:
            counts[row.count] = row._data['institution']

        return counts
