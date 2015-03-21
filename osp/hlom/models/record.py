

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
    metadata = BinaryJSONField(null=True)


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
                if record.title() and record.author():

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
        """

        return Record(
            data=bytes(self.record),
            ascii_handling='ignore',
            utf8_handling='ignore'
        )


    @property
    def query(self):

        """
        Build an Elasticsearch query string.
        """

        return sanitize_query(' '.join([
            self.pymarc.title(),
            self.pymarc.author()
        ]))


    class Meta:
        database = config.get_table_db('hlom_record')
