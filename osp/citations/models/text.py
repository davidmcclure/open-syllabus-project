

import sys
import re
import numpy as np
import hashlib
import os

from osp.common import config
from osp.common.models.base import BaseModel
from osp.common.utils import prettify

from osp.citations.hlom_corpus import HLOM_Corpus
from osp.citations.hlom_record import HLOM_Record
from osp.citations.jstor_corpus import JSTOR_Corpus
from osp.citations.jstor_record import JSTOR_Record
from osp.citations.utils import tokenize_field

from peewee import TextField
from playhouse.postgres_ext import ArrayField


class Text(BaseModel):


    # http://dublincore.org/usage/meetings/2002/05/citdcsv.html


    corpus              = TextField(index=True)
    identifier          = TextField(index=True)
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
    def title_tokens(self):

        """
        Tokenize the title.

        Returns: list
        """

        return tokenize_field(self.title)


    @property
    def author_tokens(self):

        """
        Tokenize the author (surname).

        Returns: list
        """

        return tokenize_field(self.surname)


    @property
    def hash_tokens(self):

        """
        Generate a sequence of tokens from the surname and title that forms a
        "signature" for the text.

        Returns:
            list: The hashing tokens.
        """

        # Sort the surname names.
        return sorted(self.author_tokens) + self.title_tokens


    @property
    def hash(self):

        """
        SHA1 the hash tokens.

        Returns:
            str: The deduping hash.
        """

        # Hash the tokens.
        sha1 = hashlib.sha1()
        sha1.update(' '.join(self.hash_tokens).encode('ascii', 'ignore'))
        return sha1.hexdigest()


    @property
    def queries(self):

        """
        Build a set of Elasticsearch query strings.

        Returns:
            list: The set of queries.
        """

        return [

            # <author> <title>
            self.author_tokens + self.title_tokens,

            # <title> <author>
            self.title_tokens + self.author_tokens,

        ]


    def pretty(self, field):

        """
        Prettify a field.

        Args:
            field (str)

        Returns: str|list
        """

        value = getattr(self, field)

        if not value:
            return None

        elif type(value) is list:
            return [prettify(v) for v in value]

        else:
            return prettify(value)


    @property
    def title_contains_author(self):

        """
        Does the title contain the surname tokens?

        Returns: bool
        """

        title = set(self.title_tokens)
        author = set(self.author_tokens)

        return author.issubset(title)


    def title_blacklisted(self, blacklist=[]):

        """
        Is the title blacklisted?

        Args:
            blacklist (list)

        Returns: bool
        """

        return self.title_tokens in map(tokenize_field, blacklist)
