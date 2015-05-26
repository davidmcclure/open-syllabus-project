

from osp.common.config import config
from osp.common.utils import termify
from osp.citations.hlom.counts import Counts
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.models.record import HLOM_Record
from peewee import fn


class HLOM_Record_Cited(HLOM_Record):


    class Meta:
        database = config.get_table_db('hlom_record_cited')


    @classmethod
    def copy_records(cls, min_rank=1000):

        """
        Copy in cited records.

        Args:
            min_rank (int): The cutoff for "frequent" words.
        """

        cited = (

            HLOM_Record.select()
            .join(HLOM_Citation)
            .group_by(HLOM_Record.id)

            # Coalesce duplicates.
            .distinct([HLOM_Record.metadata['deduping_hash']])
            .order_by(
                HLOM_Record.metadata['deduping_hash'],
                HLOM_Record.id
            )

        )

        counts = Counts()

        for r in cited:

            t = termify(r.marc.title())
            a = termify(r.marc.author())

            # Title and author empty.
            if not t or not a:
                continue

            # Title and author repeat words.
            if set.intersection(t, a):
                continue

            # No focused words in title.
            if counts.max_rank(t) < min_rank:
                continue

            # No focused words in author.
            if counts.max_rank(a) < min_rank:
                continue

            cls.create(**r._data)
