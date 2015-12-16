

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.models import Text
from osp.corpus.models import Document

from peewee import ForeignKeyField, CharField
from playhouse.postgres_ext import ArrayField


class Citation(BaseModel):


    text = ForeignKeyField(Text)
    document = ForeignKeyField(Document)
    tokens = ArrayField(CharField)


    class Meta:
        database = config.get_table_db('citation')
        indexes = ((('document', 'text'), True),)


    @property
    def min_freq(self):

        """
        Get the frequency of the most-infrequent term in the match tokens.

        Returns: float
        """

        pass


    @property
    def subfield(self):

        """
        Get the document's subfield, if any.

        Returns: Subfield|None
        """

        pass


    @property
    def field(self):

        """
        Get the document's field, if any.

        Returns: Field|None
        """

        pass


    @property
    def institution(self):

        """
        Get the document's institution, if any.

        Returns: Institution|None
        """

        pass
