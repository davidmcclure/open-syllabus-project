

from osp.citations.hlom.ranking import Ranking


def institution_ranks(iid, limit=500):

    """
    Get text rankings for an institution.

    Args:
        iid (int): The institution id.
    """

    r = Ranking()
    r.filter_institution(iid)

    for t in r.rank().limit(limit).naive():
        print(
            t.count,
            t.pymarc.title(),
            t.pymarc.author()
        )


def state_ranks(state, limit=500):

    """
    Get text rankings for a state.

    Args:
        state (str): The state abbreviation.
    """

    r = Ranking()
    r.filter_state(state)

    for t in r.rank().limit(limit).naive():
        print(
            t.count,
            t.pymarc.title(),
            t.pymarc.author()
        )
