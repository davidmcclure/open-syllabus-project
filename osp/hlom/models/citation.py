

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.hlom.models.record import HLOM_Record
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
    def index_institutions(cls):

        """
        Index document institutions.
        """

        query = (

            cls.select(
                cls.id,
                Institution.id.alias('iid'),
                Institution.metadata
            )

            # Join institutions.
            .join(Document_Institution, on=(
                HLOM_Citation.document==Document_Institution.document
            ))
            .join(Institution)

        )

        for c in bar(query.naive(), expected_size=query.count()):

            # Denormalize id and state.
            query = (
                HLOM_Citation
                .update(
                    institution=c.iid,
                    state=c.metadata.get('Institution_State')
                )
                .where(HLOM_Citation.id==c.id)
            )

            query.execute()
