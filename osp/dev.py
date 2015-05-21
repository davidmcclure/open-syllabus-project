

from osp.citations.hlom.ranking import Ranking


def print_rank(query):
    for t in query:
        print(t.count, t.pymarc.title(), t.pymarc.author())


def all_ranks(limit=100):

    """
    Get unfiltered rankings.
    """

    r = Ranking()
    print_rank(r.rank(1, limit))


def institution_ranks(iid, limit=100):

    """
    Get text rankings for an institution.

    Args:
        iid (int): The institution id.
    """

    r = Ranking()
    r.filter_institution(iid)
    print_rank(r.rank(1, limit))


def state_ranks(state, limit=100):

    """
    Get text rankings for a state.

    Args:
        state (str): The state abbreviation.
    """

    r = Ranking()
    r.filter_state(state)
    print_rank(r.rank(1, limit))
