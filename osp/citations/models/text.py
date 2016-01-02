

import sys
import re
import numpy as np
import hashlib
import os

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.utils import tokenize_field
from osp.citations.hlom_corpus import HLOM_Corpus
from osp.citations.hlom_record import HLOM_Record
from osp.citations.jstor_corpus import JSTOR_Corpus
from osp.citations.jstor_record import JSTOR_Record

from peewee import TextField
from playhouse.postgres_ext import ArrayField


class Text(BaseModel):


    # http://dublincore.org/usage/meetings/2002/05/citdcsv.html


    corpus              = TextField(index=True)
    identifier          = TextField()
    url                 = TextField(null=True)

    # Book + article:

    title               = TextField()
    surname             = TextField()
    authors             = ArrayField(TextField)
    publisher           = TextField(null=True)
    date                = TextField(null=True)

    # Article:

    journal_title       = TextField(null=True)
    journal_identifier  = TextField(null=True)
    issue_volume        = TextField(null=True)
    issue_number        = TextField(null=True)
    issue_chronology    = TextField(null=True)
    pagination          = TextField(null=True)


    class Meta:
        database = config.get_table_db('text')
        indexes = ((('corpus', 'identifier'), True),)


    @classmethod
    def ingest_hlom(cls):

        """
        Ingest HLOM MARC records.
        """

        corpus = HLOM_Corpus.from_env()

        for i, marc in enumerate(corpus.records()):

            try:

                record = HLOM_Record(marc)

                if record.is_queryable:

                    cls.create(
                        corpus      = 'hlom',
                        identifier  = record.control_number,
                        title       = record.title,
                        surname     = record.surname,
                        authors     = record.authors,
                        publisher   = record.publisher,
                        date        = record.date,
                    )

            except: pass

            sys.stdout.write('\r'+str(i))
            sys.stdout.flush()


    @classmethod
    def ingest_jstor(cls):

        """
        Ingest JSTOR records.
        """

        corpus = JSTOR_Corpus.from_env()

        for i, path in enumerate(corpus.paths()):

            try:

                article = JSTOR_Record(path)

                if article.is_queryable:

                    cls.create(
                        corpus              = 'jstor',
                        identifier          = article.article_id,
                        url                 = article.url,
                        title               = article.article_title,
                        surname             = article.surname,
                        authors             = article.authors,
                        publisher           = article.publisher_name,
                        date                = article.pub_date,
                        journal_title       = article.journal_title,
                        journal_identifier  = article.journal_id,
                        issue_volume        = article.volume,
                        issue_number        = article.issue,
                        pagination          = article.pagination,
                    )

            except: pass

            i += 1
            sys.stdout.write('\r'+str(i))
            sys.stdout.flush()


    @property
    def hash(self):

        """
        Create a hash that tries to merge together differently-formatted
        editions of the same text.

        Returns:
            str: The deduping hash.
        """

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

        t_tokens = tokenize_field(self.title)
        a_tokens = tokenize_field(self.authors[0])

        # Title + complete name.
        queries = [t_tokens + a_tokens]

        # Title + partial names.
        for name in a_tokens:
            queries.append(t_tokens + [name])

        return queries
