

import re

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.common.utils import query_bar
from osp.corpus.models.document import Document
from osp.corpus.utils import tokenize
from collections import Counter
from peewee import *


class Document_Text(BaseModel, Elasticsearch):


    document = ForeignKeyField(Document, unique=True)
    text = TextField()


    class Meta:
        database = config.get_table_db('document_text')


    es_index = 'osp'
    es_doc_type = 'syllabus'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True
        },
        'properties': {
            'doc_id': {
                'type': 'integer'
            },
            'body': {
                'type': 'string'
            }
        }
    }


    @classmethod
    def es_stream_docs(cls):

        """
        Index all texts.

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

        return {
            '_id':      self.document.path,
            'doc_id':   self.document.id,
            'body':     self.text
        }


    @classmethod
    def term_counts(cls):

        """
        Get frequency counts for all unique word types.

        Returns:
            dict: type -> count
        """

        counts = Counter()

        for row in query_bar(cls.select()):
            row.tokenize()
            for term, offsets in row.terms.items():
                counts[term] += len(offsets)

        return counts


    def tokenize(self):

        """
        Tokenize the text.
        """

        self.tokens = []
        self.terms  = {}

        for token in tokenize(self.text):

            # Token:
            self.tokens.append(token)

            # Word type:
            offsets = self.terms.setdefault(token['stemmed'], [])
            offsets.append(token['offset'])
