

from osp.common.config import config
from osp.citations.hlom.counts import Counts
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.models.record import HLOM_Record
from osp.corpus.utils import tokenize
from peewee import fn


class HLOM_Record_Cited(HLOM_Record):


    class Meta:
        database = config.get_table_db('hlom_record_cited')


    @classmethod
    def copy_records(cls):

        """
        Copy in cited records.
        """

        cited = (

            HLOM_Record
            .select()

            # Coalesce duplicates.
            .distinct([HLOM_Record.metadata['deduping_hash']])
            .order_by(
                HLOM_Record.metadata['deduping_hash'],
                HLOM_Record.id
            )

            .group_by(HLOM_Record.id)
            .join(HLOM_Citation)

        )

        counts = Counts()

        for r in cited:

            t = [t['stemmed'] for t in tokenize(r.marc.title())]
            a = [t['stemmed'] for t in tokenize(r.marc.author())]

            # Title and author empty.
            if not t or not a:
                continue

            # Title and author repeat words.
            if set.intersection(set(t), set(a)):
                continue

            ranks = []
            for token in set.union(set(t), set(a)):
                rank = counts.rank(token)
                if rank:
                    ranks.append(rank)

            # No infrequent terms.
            if max(ranks) < 2000:
                continue

            cls.create(**r._data)
