

import datetime

from osp.common.models.base import BaseModel
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
            cls
            .select(cls)
            .distinct([cls.document])
            .order_by(cls.document, cls.created.desc())
        )


    class Meta:
        db_table = 'document_to_institution'
