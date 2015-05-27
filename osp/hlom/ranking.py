

import numpy as np

from osp.corpus.models.tsvector import Document_TSVector
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.models.record_cited import HLOM_Record_Cited
from osp.locations.models.doc_inst import Document_Institution
from osp.institutions.models.institution import Institution
from playhouse.postgres_ext import Match
from peewee import fn


class Ranking:


    def __init__(self):

        """
        Initialize the query and ranking stats.
        """

        count = fn.Count(HLOM_Citation.id)

        self._query = (

            HLOM_Record_Cited
            .select(HLOM_Record_Cited, count)

            # Join citations.
            .join(HLOM_Citation, on=(
                HLOM_Record_Cited.id==HLOM_Citation.record
            ))

            .group_by(HLOM_Record_Cited.id)
            .order_by(count.desc())

        )


    def filter_state(self, state):

        """
        Filter by state.

        Args:
            state (str): The state abbreviation.
        """

        self._query = (
            self._query
            .where(HLOM_Citation.state==state)
        )


    def filter_institution(self, iid):

        """
        Filter by institution.

        Args:
            iid (int): The institution id.
        """

        self._query = (
            self._query
            .where(HLOM_Citation.institution==iid)
        )


    def filter_keywords(self, query, tsv_limit=1000):

        """
        Filter by keywords.

        Args:
            query (str): An free text query.
        """

        # AND-ify the query.
        query = ' & '.join(query.split())

        rank = fn.ts_rank(
            Document_TSVector.text,
            fn.to_tsquery(query)
        )

        # Select top N documents, ordered by relevance.
        matching = (
            Document_TSVector
            .select(Document_TSVector.document)
            .where(Document_TSVector.text.match(query))
            .order_by(rank.desc())
            .limit(tsv_limit)
            .alias('tsv')
        )

        # Join the subquery onto the citations.
        self._query = (
            self._query
            .join(matching, on=(
                HLOM_Citation.document==matching.c.document_id
            ))
        )


    def rank(self, page_num=1, page_len=100):

        """
        Pull the rankings, compute scores.

        Args:
            page_num (int): The (1-indexed) page number.
            page_len (int): Texts per page.

        Returns:
            peewee.SelectQuery
        """

        query = (
            self._query
            .paginate(page_num, page_len)
            .naive()
        )

        ranks = []
        for i, row in enumerate(query):

            # Overall rank.
            rank = (page_len*(page_num-1))+i+1

            ranks.append({
                'rank': rank,
                'record': row
            })

        return ranks
