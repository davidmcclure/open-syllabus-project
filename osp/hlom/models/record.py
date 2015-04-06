

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


    @property
    def pymarc(self):

        """
        Wrap the raw record blob as a Pymarc record instance.

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
            self.pymarc.title(),
            self.pymarc.author()
        ])

        # Lowercase, tokenize, sort tokens.
        tokens = sorted(re.findall('\w+', text.lower()))

        # Remove articles.
        tokens = [t for t in tokens if t not in ['a', 'an', 'the']]

        # Hash the filtered tokens.
        sha1 = hashlib.sha1()
        sha1.update(' '.join(tokens).encode('ascii', 'ignore'))
        return sha1.hexdigest()


    @property
    def es_query(self):

        """
        Build an Elasticsearch query string.

        Returns:
            str: "[title] [author]"
        """

        return sanitize_query(' '.join([
            self.pymarc.title(),
            self.pymarc.author()
        ]))


    # Denormalization routines for Elasticsearch.
    # TODO: How to do this dynamically?


    @property
    def es_doc(self):

        """
        Construct a document for Elasticsearch.

        Returns:
            dict: The document fields.
        """

        return {
            '_id':          self.control_number,
            'author':       prettify_field(self.pymarc.author()),
            'title':        prettify_field(self.pymarc.title()),
            'publisher':    prettify_field(self.pymarc.publisher()),
            'pubyear':      prettify_field(self.pymarc.pubyear()),
            'count':        self.metadata['citation_count'],
            'rank':         self.metadata['teaching_rank'],
            'percent':      self.metadata['teaching_percent']
        }


    @classmethod
    def blacklist(cls, control_number):

        """
        Exclude a record from indexing.

        Args:
            control_number (str)
        """

        record = cls.get(cls.control_number==control_number)
        record.metadata['blacklisted'] = True
        record.save()


    @classmethod
    def select_cited(cls):

        """
        Select records that have at least one citation, aren't blacklisted,
        and aren't duplicates.

        Returns:
            The filtered query.
        """

        return (

            cls.select()

            # Omit blacklisted records.
            .where(~cls.metadata.contains('blacklisted'))

            # Omit records with no citations.
            .where(cls.metadata.contains('citation_count'))

            # Coalesce duplicates.
            .distinct([cls.metadata['deduping_hash']])
            .order_by(
                cls.metadata['deduping_hash'],
                cls.id
            )

        )


    @classmethod
    def write_stats(cls):

        """
        Cache citation counts and deduping hashes.
        """

        from osp.citations.hlom.models.citation import HLOM_Citation

        for pair in query_bar(HLOM_Citation.text_counts()):

            # Write citation count / deduping hash.
            pair.record.metadata['citation_count'] = pair.count
            pair.record.metadata['deduping_hash'] = pair.record.hash
            pair.record.save()


    @classmethod
    def write_metrics(cls):

        """
        Cache teaching ranks and percentiles.
        """

        # Get record -> count tuples.
        records = list(cls.select_cited())

        # Get min/max ranks.
        counts = [r.metadata['citation_count'] for r in records]
        max_ranks = rankdata(counts, 'max')
        min_ranks = rankdata(counts, 'min')

        # Rank in ascending order.
        max_ranks = max_ranks.max()+1 - max_ranks
        min_ranks = min_ranks.max()+1 - min_ranks
        log_count = np.log(len(records))

        for i, record in enumerate(bar(records)):

            max_rank = int(max_ranks[i])
            min_rank = int(min_ranks[i])

            # Get the log ratio of the rank.
            percent = ((log_count-np.log(min_rank))/log_count)*100

            record.metadata['teaching_rank'] = max_rank
            record.metadata['teaching_percent'] = percent
            record.save()
