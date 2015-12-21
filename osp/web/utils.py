

from osp.citations.models import Citation_Index
from osp.institutions.models import Institution_Index
from osp.fields.models import Field_Index
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

    """
    Materialize subfield facets with counts.

    Returns:
        dict: {label, value, count}
    """

    counts = Citation_Index.count_facets('field_id')
    return Field_Index.materialize_facets(counts)


def institution_facets():

    """
    Materialize subfield facets with counts.

    Returns:
        dict: {label, value, count}
    """

    counts = Citation_Index.count_facets('institution_id')
    return Institution_Index.materialize_facets(counts)


def state_facets():
    pass


def country_facets():
    pass
