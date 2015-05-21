

from osp.citations.hlom.models.record_cited import HLOM_Record_Cited
from osp.citations.hlom.models.citation import HLOM_Citation


def print_rank(query):
    for t in query:
        print(t.count, t.pymarc.title(), t.pymarc.author())


def all_ranks(page_num=1, page_len=100):

    """
    Get unfiltered rankings.
    """

    query = (
        HLOM_Record_Cited.rank()
        .paginate(page_num, page_len)
    )

    print_rank(query)


def institution_ranks(iid, page_num=1, page_len=100):

    """
    Get text rankings for an institution.

    Args:
        iid (int): The institution id.
    """

    query = (
        HLOM_Record_Cited.rank()
        .where(HLOM_Citation.institution==iid)
        .paginate(page_num, page_len)
    )

    print_rank(query)


def state_ranks(state, page_num=1, page_len=100):

    """
    Get text rankings for a state.

    Args:
        state (str): The state abbreviation.
    """

    query = (
        HLOM_Record_Cited.rank()
        .where(HLOM_Citation.state==state)
        .paginate(page_num, page_len)
    )

    print_rank(query)
