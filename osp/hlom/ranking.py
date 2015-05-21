

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.models.record_cited import HLOM_Record_Cited
from osp.locations.models.doc_inst import Document_Institution
from osp.institutions.models.institution import Institution
from peewee import fn


class Ranking:


    def __init__(self):

        """
        Initialize the un-filtered query.
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


    def rank(self, page_num=1, page_len=100):

        """
        Pull the rankings.

        Args:
            page_num (int): The (1-indexed) page number.
            page_len (int): Texts per page.

        Returns:
            peewee.SelectQuery
        """

        return (
            self._query
            .paginate(page_num, page_len)
            .naive()
        )
