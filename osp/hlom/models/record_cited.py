

from osp.common.config import config
from osp.common.utils import termify, query_bar
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.hlom.counts import Counts
from osp.hlom.models.citation import HLOM_Citation
from osp.hlom.models.record import HLOM_Record
from osp.hlom.utils import prettify_field
from scipy.stats import rankdata
from peewee import fn


class HLOM_Record_Cited(HLOM_Record, Elasticsearch):


    class Meta:
        database = config.get_table_db('hlom_record_cited')


    es_index = 'osp'
    es_doc_type = 'record'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True
        },
        'properties': {
            'author': {
                'type': 'string'
            },
            'title': {
                'type': 'string'
            },
            'publisher': {
                'type': 'string'
            },
            'count': {
                'type': 'integer'
            },
            'rank': {
                'type': 'integer'
            }
        }
    }


    @classmethod
    def es_stream_docs(cls):

        """
        Index all rows.

        Yields:
            dict: The next document.
        """

        for row in query_bar(cls.select()):
            yield row.es_doc


    @property
    def es_doc(self):

        """
        Construct a document for Elasticsearch.

        Returns:
            dict: The document fields.
        """

        return {
            '_id':          self.control_number,
            'author':       prettify_field(self.marc.author()),
            'title':        prettify_field(self.marc.title()),
            'publisher':    prettify_field(self.marc.publisher()),
            'count':        self.metadata['citation_count'],
            'rank':         self.metadata['rank'],
        }


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


    @classmethod
    def rank(cls):

        """
        Write citation counts and ranks.
        """

        count = fn.COUNT(HLOM_Citation.id)

        query = (
            cls.select(cls, count)
            .join(HLOM_Citation, on=(HLOM_Citation.record==cls.id))
            .order_by(count.desc())
            .group_by(cls.id)
        )

        # Get up citation counts.
        counts = [r.count for r in query]

        # Rank in ascending order.
        ranks = rankdata(counts, 'max')
        ranks = ranks.max()+1 - ranks

        for i, r in enumerate(query_bar(query)):
            r.metadata['citation_count'] = counts[i]
            r.metadata['rank'] = int(ranks[i])
            r.save()
