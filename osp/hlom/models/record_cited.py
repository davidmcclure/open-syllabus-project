

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

            t = [t['stemmed'] for t in tokenize(r.marc.title())]
            a = [t['stemmed'] for t in tokenize(r.marc.author())]

            # Title and author empty.
            if not t or not a:
                continue

            # Title and author repeat words.
            if set.intersection(set(t), set(a)):
                continue

            t_ranks = []
            for token in set(t):
                rank = counts.rank(token)
                if rank:
                    t_ranks.append(rank)

            a_ranks = []
            for token in set(a):
                rank = counts.rank(token)
                if rank:
                    a_ranks.append(rank)

            # Gather the ranks for all terms.
            #ranks = []
            #for token in set.union(set(t), set(a)):
                #rank = counts.rank(token)
                #if rank:
                    #ranks.append(rank)

            if t_ranks and max(t_ranks) < min_rank:
                continue

            if a_ranks and max(a_ranks) < min_rank:
                continue

            # No infrequent terms.
            #if max(ranks) < min_rank:
                #continue

            cls.create(**r._data)
