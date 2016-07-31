

from osp.common import config
from osp.common.models import BaseModel
from osp.corpus.models import Document
from osp.citations.models import Text

from osp.institutions.models import Institution
from osp.institutions.models import Institution_Document
from osp.fields.models import Subfield
from osp.fields.models import Subfield_Document

from playhouse.postgres_ext import ArrayField
from peewee import ForeignKeyField, CharField


class Citation(BaseModel):


    text = ForeignKeyField(Text)
    document = ForeignKeyField(Document)
    tokens = ArrayField(CharField)


    class Meta:
        database = config.get_table_db('citation')
        indexes = ((('document', 'text'), True),)


    @property
    def subfield(self):

        """
        Get the document's subfield, if any.

        Returns: Subfield
        """

        return (
            Subfield
            .select()
            .join(Subfield_Document)
            .join(Document)
            .where(Document.id==self.document)
            .order_by(Subfield_Document.offset.asc())
            .first()
        )


    @property
    def institution(self):

        """
        Get the document's institution, if any.

        Returns: Institution
        """

        return (
            Institution
            .select()
            .join(Institution_Document)
            .join(Document)
            .where(Document.id==self.document)
            .first()
        )
