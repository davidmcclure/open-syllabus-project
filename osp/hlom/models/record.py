

import sys

from osp.common.config import config
from osp.common.models.base import BaseModel
from osp.citations.hlom.dataset import Dataset
from osp.citations.hlom.utils import sanitize_query
from pymarc import Record
from playhouse.postgres_ext import *
from peewee import *


class HLOM_Record(BaseModel):


    control_number = CharField(unique=True, null=False)
    record = BlobField(null=False)
    metadata = BinaryJSONField(default={})


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
    def write_citation_count(cls):

        """
        Write a `citation_count` field into the metadata field.
        """

        from osp.citations.hlom.models.citation import HLOM_Citation

        for pair in HLOM_Citation.text_counts():

            # Write on the citation count.
            pair.record.metadata['citation_count'] = pair.count
            pair.record.save()


    @classmethod
    def write_deduping_hash(cls):
        pass


    @classmethod
    def write_teaching_rank(cls):
        pass


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


    @property
    def pymarc(self):

        """
        Wrap the raw record blob as a Pymarc record instance.
        """

        return Record(
            data=bytes(self.record),
            ascii_handling='ignore',
            utf8_handling='ignore'
        )


    @property
    def author(self):

        """
        Get an Elasticsearch-sanitized author.
        """

        return sanitize_query(self.pymarc.author())


    @property
    def title(self):

        """
        Get an Elasticsearch-sanitized title.
        """

        return sanitize_query(self.pymarc.title())


    class Meta:
        database = config.get_table_db('hlom_record')
