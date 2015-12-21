

from osp.citations.models import Citation_Index
from osp.fields.models import Subfield_Index


def rank_texts():
    pass


def assigned_with():
    pass


def corpus_facets():
    pass


def subfield_facets():

    """
    Materialize subfield facets with counts.

    Returns:
        dict: {label, value, count}
    """

    counts = Citation_Index.count_facets('subfield_id')
    return Subfield_Index.materialize_facets(counts)


def field_facets():
    pass


def institution_facets():
    pass


def state_facets():
    pass


def country_facets():
    pass
