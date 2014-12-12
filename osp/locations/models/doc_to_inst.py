

import datetime

from osp.locations.models.base import BaseModel
from osp.institutions.models.institution import Institution
from peewee import *


class DocToInst(BaseModel):


    created     = DateTimeField(default=datetime.datetime.now)
    institution = ForeignKeyField(Institution)
    document    = CharField()


    @classmethod
    def select_current(cls):

        """
        Select the current associations.
        """

        return (
            DocToInst
            .select(DocToInst)
            .distinct([DocToInst.document])
            .order_by(DocToInst.document, DocToInst.created.desc())
        )


    class Meta:
        db_table = 'document_to_institution'
