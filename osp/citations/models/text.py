

import sys
import re
import numpy as np
import hashlib

from osp.common.config import config
from osp.common.utils import query_bar
from osp.common.models.base import BaseModel
from osp.citations.utils import prettify_field
from osp.citations.hlom_corpus import HLOM_Corpus
from osp.citations.utils import sanitize_query
from pymarc import Record
from clint.textui.progress import bar

from playhouse.postgres_ext import BinaryJSONField
from peewee import CharField, BlobField


class Text(BaseModel):


    control_number = CharField(unique=True, null=False)
    record = BlobField(null=False)
    metadata = BinaryJSONField(default={})


    class Meta:
        database = config.get_table_db('text')


    @classmethod
    def ingest_hlom(cls, page_size=10000):

        """
        Insert an row for each record in the HLOM corpus.

        Args:
            page_size (int): Batch-insert page size.
        """

        dataset = HLOM_Corpus.from_env()

        i = 0
        for group in dataset.grouped_records(page_size):

            rows = []
            for record in group:

                # Require title and author.
                if record and record.title() and record.author():

                    rows.append({
                        'control_number': record['001'].format_field(),
                        'record': record.as_marc()
                    })

            if rows:
                Text.insert_many(rows).execute()

            i += 1
            sys.stdout.write('\r'+str(page_size*i))
            sys.stdout.flush()


    @classmethod
    def dedupe(cls):

        """
        Write deduping hashes.
        """

        from .citation import Citation

        cited = (
            cls.select()
            .join(Citation)
            .group_by(cls.id)
        )

        for record in query_bar(cited):
            record.metadata['deduping_hash'] = record.hash
            record.save()


    @property
    def marc(self):

        """
        Wrap the MARC blob as a Pymarc instance.

        Returns:
            pymarc.Record
        """

        return Record(
            data=bytes(self.record),
            ascii_handling='ignore',
            utf8_handling='ignore'
        )


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
            self.marc.title(),
            self.marc.author()
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
