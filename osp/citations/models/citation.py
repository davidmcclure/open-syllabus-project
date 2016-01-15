

import sys
import numpy as np

from osp.common import config
from osp.common.utils import query_bar
from osp.common.models.base import BaseModel
from osp.corpus.models import Document
from osp.citations.models import Text

from osp.institutions.models import Institution
from osp.institutions.models import Institution_Document
from osp.fields.models import Subfield
from osp.fields.models import Subfield_Document

from functools import reduce
from playhouse.postgres_ext import ArrayField, ServerSide
from peewee import ForeignKeyField, CharField, BooleanField
from wordfreq import word_frequency


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


    @property
    def fuzz(self):

        """
        Compute an arbitrarily-scaled "fuzziness" score for the citation
        tokens, where low is focused and high is fuzzy.

        Returns: float
        """

        freqs = [
            word_frequency(t, 'en', minimum=1e-6)
            for t in self.tokens
        ]

        return reduce(lambda x, y: x*y, freqs)*1e10
