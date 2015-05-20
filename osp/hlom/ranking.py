

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

        self.query = (

            HLOM_Record_Cited
            .select(HLOM_Record_Cited, count)

            # Join citations.
            .join(HLOM_Citation, on=(
                HLOM_Record_Cited.id==HLOM_Citation.record
            ))

            .group_by(HLOM_Record_Cited.id)
            .order_by(count.desc())

        )


    def filter_institution(self, iid):

        """
        Filter by institution.

        Args:
            iid (int): The institution id.
        """

        pass


    def filter_state(self, state):

        """
        Filter by state.

        Args:
            state (str): The state abbreviation.
        """

        pass


    def rank(self):

        """
        Pull the rankings.

        Returns:
            peewee.SelectQuery
        """

        pass
