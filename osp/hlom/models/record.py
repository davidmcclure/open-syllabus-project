

import sys
import re
import numpy as np
import hashlib

from osp.common.config import config
from osp.common.utils import query_bar
from osp.common.models.base import BaseModel
from osp.citations.hlom.utils import prettify_field
from osp.citations.hlom.dataset import Dataset
from osp.citations.hlom.utils import sanitize_query
from pymarc import Record
from scipy.stats import rankdata
from clint.textui.progress import bar
from playhouse.postgres_ext import *
from peewee import *


class HLOM_Record(BaseModel):


    control_number = CharField(unique=True, null=False)
    record = BlobField(null=False)
    metadata = BinaryJSONField(default={})


    class Meta:
        database = config.get_table_db('hlom_record')


    @classmethod
    def insert_records(cls, page_size=10000):

        """
        Insert an row for each record in the HLOM corpus.

        Args:
            page_size (int): Batch-insert page size.
        """

        dataset = Dataset.from_env()

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
                HLOM_Record.insert_many(rows).execute()

            i += 1
            sys.stdout.write('\r'+str(page_size*i))
            sys.stdout.flush()


    @classmethod
    def write_stats(cls):

        """
        Write deduping hashes and citation counts.
        """

        from .citation import HLOM_Citation

        count = fn.COUNT(HLOM_Citation.id)

        cited = (
            cls.select(cls, count)
            .join(HLOM_Citation)
            .group_by(cls.id)
        )

        for r in query_bar(cited):
            r.metadata['deduping_hash'] = r.hash
            r.metadata['citation_count'] = r.count
            r.save()


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
