

import sys
import re
import numpy as np
import hashlib

from osp.common.config import config
from osp.common.utils import query_bar
from osp.common.models.base import BaseModel
from osp.citations.utils import prettify_field, sanitize_query
from osp.citations.hlom_corpus import HLOM_Corpus
from pymarc import Record
from clint.textui.progress import bar

from peewee import CharField


class Text(BaseModel):


    title       = CharField()
    author      = CharField()
    publisher   = CharField(null=True)
    date        = CharField(null=True)
    journal     = CharField(null=True)


    class Meta:
        database = config.get_table_db('text')


    @classmethod
    def ingest_hlom(cls, page_size=10000):

        """
        Ingest the HLOM MARC records.

        Args:
            page_size (int): Batch-insert page size.
        """

        pass


    @property
    def hash(self):

        """
        Create a hash that tries to merge together differently-formatted
        editions of the same text.

        Returns:
            str: The deduping hash.
        """

        # Get "[title] [author]".
        text = ' '.join([
            self.title,
            self.author,
        ])

        # Lowercase, tokenize, sort tokens.
        tokens = sorted(re.findall('[a-z]+', text.lower()))

        # Remove articles.
        tokens = [t for t in tokens if t not in ['a', 'an', 'the']]

        # Hash the filtered tokens.
        sha1 = hashlib.sha1()
        sha1.update(' '.join(tokens).encode('ascii', 'ignore'))
        return sha1.hexdigest()


    @property
    def query(self):

        """
        Build an Elasticsearch query string.

        Returns:
            str|None: "[title] [author]", or None if invalid.
        """

        t = sanitize_query(self.marc.title())
        a = sanitize_query(self.marc.author())

        return t+' '+a
