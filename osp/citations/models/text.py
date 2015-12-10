

import sys
import re
import numpy as np
import hashlib

from osp.common.config import config
from osp.common.utils import query_bar
from osp.common.models.base import BaseModel
from osp.citations.hlom_corpus import HLOM_Corpus
from osp.citations.utils import tokenize_query, tokenize_field
from pymarc import Record
from clint.textui.progress import bar

from peewee import CharField


class Text(BaseModel):


    identifier  = CharField(unique=True)
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
        Ingest HLOM MARC records.

        Args:
            page_size (int): Batch-insert page size.
        """

        corpus = HLOM_Corpus.from_env()

        for group in corpus.grouped_records(page_size):

            rows = []
            for record in group:

                tokens = tokenize_query(
                    record.title(),
                    record.author()
                )

                # Require a query-able title and author.
                if len(tokens) >= 2:

                    rows.append({
                        'identifier':   record['001'].format_field(),
                        'title':        record.title(),
                        'author':       record.author(),
                        'publisher':    record.publisher(),
                        'date':         record.pubyear(),
                    })

            if rows:
                cls.insert_many(rows).execute()


    @classmethod
    def ingest_jstor(cls, page_size=10000):

        """
        Ingest JSTOR records.

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

        # Extract tokens.
        t_tokens = tokenize_field(self.title)
        a_tokens = tokenize_field(self.author)

        # Sort the author names.
        tokens = t_tokens + sorted(a_tokens)

        # Hash the tokens.
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

        tokens = tokenize_query(self.title, self.author)

        return ' '.join(tokens)
