

import sys
import re
import numpy as np
import hashlib
import os

from osp.common import config
from osp.common.utils import prettify, query_bar
from osp.common.models.base import BaseModel

from osp.constants import redis_keys
from osp.citations.utils import tokenize_field, is_toponym
from osp.citations.jstor_corpus import JSTOR_Corpus
from osp.citations.jstor_record import JSTOR_Record
from osp.citations.hlom_corpus import HLOM_Corpus
from osp.citations.hlom_record import HLOM_Record
from osp.citations.validate_config import Validate_Config

from functools import reduce
from peewee import TextField, BooleanField
from playhouse.postgres_ext import ArrayField
from wordfreq import word_frequency


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

    # Validation:

    valid               = BooleanField(null=True, index=True)
    display             = BooleanField(null=True, index=True)


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


    @classmethod
    def select_cited(cls):

        """
        Select texts with at least one citation.

        Returns: peewee.SelectQuery
        """

        from . import Citation

        return (
            cls
            .select()
            .join(Citation)
            .order_by(cls.id)
            .group_by(cls.id)
        )


    @classmethod
    def deduplicate(cls):

        """
        Deduplicate cited texts.
        """

        for text in query_bar(cls.select_cited()):

            # Has the hash been seen?
            seen = config.redis.sismember(
                redis_keys.OSP_DEDUP,
                text.hash,
            )

            # If so, don't display this text.
            if seen:
                text.display = False

            else:

                # If not, display this text.
                text.display = True

                # And reserve the hash.
                config.redis.sadd(
                    redis_keys.OSP_DEDUP,
                    text.hash,
                )

            text.save()


    @classmethod
    def validate(cls, *args, **kwargs):

        """
        Validate all cited texts.
        """

        config = Validate_Config(*args, **kwargs)

        for text in query_bar(cls.select_cited()):

            text.valid = not (

                # Title
                text.title_contains_surname or
                text.title_blacklisted(config.blacklisted_titles) or
                text.title_is_toponym or

                # Surname
                text.surname_blacklisted(config.blacklisted_surnames) or
                text.surname_is_toponym or

                # Focus
                text.unfocused(config.max_fuzz)

            )

            text.save()


    @property
    def title_tokens(self):

        """
        Tokenize the title.

        Returns: list
        """

        return tokenize_field(self.title)


    @property
    def surname_tokens(self):

        """
        Tokenize the surname.

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

        # Sort the surname tokens.
        return sorted(self.surname_tokens) + self.title_tokens


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
            self.surname_tokens + self.title_tokens,

            # <title> <author>
            self.title_tokens + self.surname_tokens,

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
    def fuzz(self):

        """
        Compute an arbitrarily-scaled "fuzziness" score for the query tokens,
        where low is focused and high is fuzzy.

        Returns: float
        """

        freqs = [
            word_frequency(t, 'en', minimum=1e-6)
            for t in self.hash_tokens
        ]

        return reduce(lambda x, y: x*y, freqs)*1e10


    @property
    def title_contains_surname(self):

        """
        Does the title contain the surname tokens?

        Returns: bool
        """

        title = set(self.title_tokens)
        surname = set(self.surname_tokens)

        return surname.issubset(title)


    def title_blacklisted(self, blacklist=[]):

        """
        Is the title blacklisted?

        Args:
            blacklist (list)

        Returns: bool
        """

        return self.title_tokens in blacklist


    def surname_blacklisted(self, blacklist=[]):

        """
        Is the surname blacklisted?

        Args:
            blacklist (list)

        Returns: bool
        """

        return self.surname_tokens in blacklist


    @property
    def title_is_toponym(self):

        """
        Is the title the name of a country or US state?

        Returns: bool
        """

        title = ' '.join(self.title_tokens)
        return is_toponym(title)


    @property
    def surname_is_toponym(self):

        """
        Is the surname the name of a country or US state?

        Returns: bool
        """

        surname = ' '.join(self.surname_tokens)
        return is_toponym(surname)


    def unfocused(self, max_fuzz=float('inf')):

        """
        Are the title / surname tokens too "fuzzy" for inclusion?

        Args:
            max_fuzz (float)

        Returns: bool
        """

        return self.fuzz > max_fuzz
