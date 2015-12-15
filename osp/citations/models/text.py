

import sys
import re
import numpy as np
import hashlib
import os

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.common.utils import grouper

from osp.citations.utils import tokenize_field, get_min_freq
from osp.citations.hlom_corpus import HLOM_Corpus
from osp.citations.jstor_article import JSTOR_Article
from osp.citations.hlom_record import HLOM_Record

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
    def ingest_hlom(cls, page_size=10000):

        """
        Ingest HLOM MARC records.

        Args:
            page_size (int)
        """

        corpus = HLOM_Corpus.from_env()

        i = 0
        for group in grouper(corpus.records(), page_size):

            rows = []
            for marc in group:

                try:

                    record = HLOM_Record(marc)

                    if record.is_queryable:

                        rows.append(dict(
                            corpus      = 'hlom',
                            identifier  = record.control_number,
                            title       = record.title,
                            author      = record.author,
                            publisher   = record.publisher,
                            date        = record.date,
                        ))

                except: pass

            if rows:
                cls.insert_many(rows).execute()

            i += 1
            sys.stdout.write('\r'+str(page_size*i))
            sys.stdout.flush()


    @classmethod
    def ingest_jstor(cls, page_size=10000):

        """
        Ingest JSTOR records.

        Args:
            page_size (int)
        """

        paths = os.walk(config['jstor']['corpus'])

        i = 0
        for group in grouper(paths, page_size):

            rows = []
            for root, dirs, files in group:
                for name in files:

                    try:

                        path = os.path.join(root, name)
                        article = JSTOR_Article(path)

                        if article.is_queryable:

                            rows.append(dict(
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
                            ))

                    except: pass

            if rows:
                cls.insert_many(rows).execute()

            i += 1
            sys.stdout.write('\r'+str(page_size*i))
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
