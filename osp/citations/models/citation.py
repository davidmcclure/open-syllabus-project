

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.common.utils import query_bar
from osp.citations.models import Text
from osp.corpus.models import Document

from osp.fields.models import Subfield
from osp.fields.models import Subfield_Document

from osp.institutions.models import Institution
from osp.institutions.models import Institution_Document

from peewee import ForeignKeyField, CharField
from playhouse.postgres_ext import ArrayField
from wordfreq import word_frequency


class Citation(BaseModel, Elasticsearch):


    text = ForeignKeyField(Text)
    document = ForeignKeyField(Document)
    tokens = ArrayField(CharField)


    class Meta:
        database = config.get_table_db('citation')
        indexes = ((('document', 'text'), True),)


    es_index = 'osp'
    es_doc_type = 'citation'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True,
        },
        'properties': {
            'text_id': {
                'type': 'integer'
            },
            'document_id': {
                'type': 'integer'
            },
            'corpus': {
                'type': 'string'
            },
            'min_freq': {
                'type': 'float'
            },
            'subfield_id': {
                'type': 'integer'
            },
            'field_id': {
                'type': 'integer'
            },
            'institution_id': {
                'type': 'integer'
            },
        }
    }


    @classmethod
    def es_stream_docs(cls):

        """
        Stream Elasticsearch docs.

        Yields:
            dict: The next document.
        """

        for row in query_bar(cls.select()):
            yield row.es_doc


    @property
    def es_doc(self):

        """
        Construct a document for Elasticsearch.

        Returns:
            dict: The document fields.
        """

        doc = {}

        # Local fields:

        doc['_id'] = self.id
        doc['text_id'] = self.text_id
        doc['document_id'] = self.document_id
        doc['corpus'] = self.text.corpus
        doc['min_freq'] = self.min_freq

        # Field references:

        subfield = self.subfield

        if subfield:
            doc['subfield_id'] = subfield.id
            doc['field_id'] = subfield.field_id

        # Institution reference:

        inst = self.institution

        if inst:
            doc['institution_id'] = inst.id

        return doc


    @property
    def min_freq(self):

        """
        Get the frequency of the most-infrequent term in the match tokens.

        Returns: float
        """

        freqs = [word_frequency(t, 'en') for t in self.tokens]

        return min(freqs) * 1e6


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
