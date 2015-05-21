

from osp.citations.hlom.ranking import Ranking
from osp.citations.hlom.models.record_cited import HLOM_Record_Cited
from playhouse.postgres_ext import ServerSide


r = Ranking()


def print_rank(query):
    for t in query:
        print(
            t['rank'],
            t['record'].count,
            round(t['score'], 2),
            t['record'].marc.title(),
            t['record'].marc.author()
        )


def all_ranks(page_num=1, page_len=100):

    """
    Get unfiltered rankings.
    """

    r.reset()
    print_rank(r.rank(page_num, page_len))


def institution_ranks(iid, page_num=1, page_len=100):

    """
    Get text rankings for an institution.

    Args:
        iid (int): The institution id.
    """

    r.reset()
    r.filter_institution(iid)
    print_rank(r.rank(page_num, page_len))


def state_ranks(state, page_num=1, page_len=100):

    """
    Get text rankings for a state.

    Args:
        state (str): The state abbreviation.
    """

    r.reset()
    r.filter_state(state)
    print_rank(r.rank(page_num, page_len))


def queries():

    """
    Print Elasticsearch queries.
    """

    for r in ServerSide(HLOM_Record_Cited.select()):
        q = r.query
        if not q:
            print(r.marc.title(), r.marc.author())
