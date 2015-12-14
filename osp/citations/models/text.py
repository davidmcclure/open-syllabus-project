

import sys
import re
import numpy as np
import hashlib
import os

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.utils import tokenize_field, get_min_freq
from osp.citations.hlom_corpus import HLOM_Corpus
from osp.citations.jstor_article import JSTOR_Article

from peewee import CharField
from playhouse.postgres_ext import ArrayField


class Text(BaseModel):


    # http://dublincore.org/usage/meetings/2002/05/citdcsv.html


    corpus              = CharField(index=True)
    identifier          = CharField(unique=True)

    # Book + article:

    title               = CharField()
    author              = ArrayField(CharField)
    publisher           = CharField(null=True)
    date                = CharField(null=True)

    # Article:

    journal_title       = CharField(null=True)
    journal_identifier  = CharField(null=True)
    issue_volume        = CharField(null=True)
    issue_number        = CharField(null=True)
    issue_chronology    = CharField(null=True)
    pagination          = CharField(null=True)


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

                t_tokens = tokenize_field(record.title())
                a_tokens = tokenize_field(record.author())

                # Require a query-able title / author.
                if t_tokens and a_tokens:

                    cls.create(
                        corpus      = 'hlom',
                        identifier  = record['001'].format_field(),
                        title       = record.title(),
                        author      = [record.author()],
                        publisher   = record.publisher(),
                        date        = record.pubyear(),
                    )

            except: pass

            sys.stdout.write('\r'+str(i))
            sys.stdout.flush()


    @classmethod
    def ingest_jstor(cls):

        """
        Ingest JSTOR records.
        """

        for root, dirs, files in os.walk(config['jstor']['corpus']):
            for name in files:

                path = os.path.join(root, name)
                article = JSTOR_Article(path)

                cls.create(
                    corpus              = 'jstor',
                    identifier          = article.article_id,
                    title               = article.article_title,
                    author              = article.author,
                    publisher           = article.publisher_name,
                    date                = article.pub_date,
                    journal_title       = article.journal_title,
                    journal_identifier  = article.journal_id,
                    issue_volume        = article.volume,
                    issue_number        = article.issue,
                    pagination          = article.pagination,
                )


    @property
    def hash(self):

        """
        Create a hash that tries to merge together differently-formatted
        editions of the same text.

        Returns:
            str: The deduping hash.
        """

        t_tokens = tokenize_field(self.title)
        a_tokens = tokenize_field(self.author[0])

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
        a_tokens = tokenize_field(self.author[0])

        # Title + complete name.
        queries = [t_tokens + a_tokens]

        # Title + partial names.
        for name in a_tokens:
            queries.append(t_tokens + [name])

        return queries
