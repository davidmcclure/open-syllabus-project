

from osp.citations.models import Citation_Index
from osp.citations.models import Text_Index
from osp.institutions.models import Institution_Index
from osp.fields.models import Field_Index
from osp.fields.models import Subfield_Index

from osp.common import config
from osp.www.cache import cache


def corpus_facets():

    """
    Materialize corpus facets with counts.

    Returns:
        dict: {label, value, count}
    """

    counts = Citation_Index.count_facets('corpus')
    return Text_Index.materialize_corpus_facets(counts)


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
    Materialize field facets with counts.

    Returns:
        dict: {label, value, count}
    """

    counts = Citation_Index.count_facets('field_id')
    return Field_Index.materialize_facets(counts)


def institution_facets(depth=200, include=None):

    """
    Materialize institution facets with counts.

    Args:
        depth (int)
        include (list)

    Returns:
        dict: {label, value, count}
    """

    counts1 = Citation_Index.count_facets('institution_id', depth=depth)

    facets1 = Institution_Index.materialize_institution_facets(counts1)

    counts2 = Citation_Index.count_facets('institution_id', include=include)

    facets2 = Institution_Index.materialize_institution_facets(counts2)

    ids = set([f['value'] for f in facets1])
    for f in facets2:
        if f['value'] not in ids:
            facets1.append(f)

    facets = sorted(
        facets1,
        key=lambda x: x['count'],
        reverse=True,
    )

    return facets


def state_facets():

    """
    Materialize state facets with counts.

    Returns:
        dict: {label, value, count}
    """

    counts = Citation_Index.count_facets('state')
    return Institution_Index.materialize_state_facets(counts)


def country_facets():

    """
    Materialize state facets with counts.

    Returns:
        dict: {label, value, count}
    """

    counts = Citation_Index.count_facets('country')
    return Institution_Index.materialize_country_facets(counts)


@cache.memoize(unless=config.is_test)
def bootstrap_facets():

    """
    Bootstrap all facets for the front-end.
    """

    return dict(
        corpus      = corpus_facets(),
        subfield    = subfield_facets(),
        field       = field_facets(),
        institution = institution_facets(),
        state       = state_facets(),
        country     = country_facets(),
    )
