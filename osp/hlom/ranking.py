

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.models.record import HLOM_Record
from osp.locations.models.doc_inst import Document_Institution
from osp.institutions.models.institution import Institution
from peewee import fn


class Ranking:


    def __init__(self):

        """
        Initialize the list of document id sets.
        """

        self.doc_ids = []


    def filter_institution(self, iid):

        """
        Filter by institution.

        Args:
            iid (int): The institution id.
        """

        docs = (
            Document_Institution
            .select()
            .where(Document_Institution.institution==iid)
        )

        ids = set([d._data['document'] for d in docs])
        self.doc_ids.append(ids)


    def filter_state(self, state):

        """
        Filter by state.

        Args:
            state (str): The state abbreviation.
        """

        institutions = (
            Institution
            .select()
            .where(Institution.metadata.contains({
                'Institution_State': state
            }))
        )

        inst_ids = [i.id for i in institutions]

        docs = (
            Document_Institution
            .select()
            .where(Document_Institution.institution << inst_ids)
        )

        ids = set([d._data['document'] for d in docs])
        self.doc_ids.append(ids)


    def rank(self):

        """
        Intersect the selected documents, pull the rankings.

        Returns:
            peewee.SelectQuery: An un-limited HLOM record query.
        """

        doc_ids = list(set.intersection(*self.doc_ids))
        count = fn.Count(HLOM_Citation.id)

        return (

            HLOM_Record
            .select(HLOM_Record, count)

            # Coalesce duplicates.
            .distinct([
                HLOM_Record.metadata['deduping_hash'],
                count
            ])
            .order_by(
                HLOM_Record.metadata['deduping_hash'],
                HLOM_Record.id
            )

            .group_by(HLOM_Record.id)
            .join(HLOM_Citation)
            .where(HLOM_Citation.document << doc_ids)
            .order_by(count.desc())

        )
