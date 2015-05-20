

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.hlom.models.record import HLOM_Record
from osp.locations.models.doc_inst import Document_Institution
from osp.institutions.models.institution import Institution
from osp.corpus.models.document import Document
from clint.textui.progress import bar
from playhouse.postgres_ext import *
from peewee import *


class HLOM_Citation(BaseModel):


    document = ForeignKeyField(Document)
    record = ForeignKeyField(HLOM_Record)

    # Ranking metadata:
    state = CharField(max_length=2, index=True, null=True)
    institution = ForeignKeyField(Institution, null=True)


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


    @classmethod
    def index_states(cls):

        """
        Index document states.
        """

        query = (

            cls
            .select(cls.id, Institution.metadata)

            # Join institutions.
            .join(Document_Institution, on=(
                HLOM_Citation.document==Document_Institution.document
            ))
            .join(Institution)

        )

        size = query.count()
        for s in bar(query.naive(), expected_size=size):

            # Denormalize the states.
            query = (
                HLOM_Citation
                .update(state=s.metadata['Institution_State'])
                .where(HLOM_Citation.id==s.id)
            )

            query.execute()


    @classmethod
    def index_institutions(cls):

        """
        Index document institutions.
        """

        query = (

            cls
            .select(cls.id, Institution.id.alias('iid'))

            # Join institutions.
            .join(Document_Institution, on=(
                HLOM_Citation.document==Document_Institution.document
            ))
            .join(Institution)

        )

        size = query.count()
        for s in bar(query.naive(), expected_size=size):

            # Denormalize the states.
            query = (
                HLOM_Citation
                .update(institution=s.iid)
                .where(HLOM_Citation.id==s.id)
            )

            query.execute()
