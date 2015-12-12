

import sys
import re
import numpy as np
import hashlib

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.utils import tokenize_field, get_min_freq
from osp.citations.hlom_corpus import HLOM_Corpus

from peewee import CharField
from playhouse.postgres_ext import ArrayField


class Text(BaseModel):


    corpus      = CharField(index=True)
    identifier  = CharField(unique=True)

    title       = CharField()
    authors     = ArrayField(CharField)
    publisher   = CharField(null=True)
    date        = CharField(null=True)
    journal     = CharField(null=True)
    url         = CharField(null=True)


    class Meta:
        database = config.get_table_db('text')


    @classmethod
    def ingest_hlom(cls):

        """
        Ingest HLOM MARC records.
        """

        corpus = HLOM_Corpus.from_env()

        for i, record in enumerate(corpus.records()):

            try:

                # Extract title / author tokens.
                t_tokens = tokenize_field(record.title())
                a_tokens = tokenize_field(record.author())

                # Require a query-able title / author.
                if t_tokens and a_tokens:

                    cls.create(
                        corpus      = 'hlom',
                        identifier  = record['001'].format_field(),
                        title       = record.title(),
                        authors     = [record.author()],
                        publisher   = record.publisher(),
                        date        = record.pubyear(),
                    )

            except: pass

            sys.stdout.write('\r'+str(i))
            sys.stdout.flush()


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
        a_tokens = tokenize_field(self.authors[0])

        # Sort the author names.
        tokens = t_tokens + sorted(a_tokens)

        # Hash the tokens.
        sha1 = hashlib.sha1()
        sha1.update(' '.join(tokens).encode('ascii', 'ignore'))
        return sha1.hexdigest()


    @property
    def queries(self):

        """
        Build a set of Elasticsearch query strings.

        Returns:
            list: The set of queries.
        """

        # Extract tokens.
        t_tokens = tokenize_field(self.title)
        a_tokens = tokenize_field(self.authors[0])

        # Title + complete name.
        seqs = [t_tokens + a_tokens]

        # Title + partial names.
        for name in a_tokens:
            seqs.append(t_tokens + [name])

        # Pair with min frequency score.
        queries = []
        for s in seqs:
            queries.append((' '.join(s), get_min_freq(s)))

        return queries
