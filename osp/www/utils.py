

from osp.citations.models import Citation_Index
from osp.citations.models import Text
from osp.citations.models import Text_Index
from osp.institutions.models import Institution_Index
from osp.fields.models import Field_Index
from osp.fields.models import Subfield_Index


def rank_texts(filters={}, query=None, size=1000):

    """
    Filter and rank texts.

    Args:
        filters (dict): Citation metadata filters.
        query (str): A text metadata search query.

    Returns:
        dict: Elasticsearch hits.
    """

    # Filter and rank the texts.
    ranks = Citation_Index.compute_ranking(filters)

    # Materialize the text metadata.
    texts = Text_Index.materialize_ranking(ranks, query, size)

    return texts


def assigned_with(corpus, identifier):

    """
    Given a "seed" text, rank other texts assigned on the same syllabi.

    Args:
        corpus (str): The corpus slug.
        identifier (str): The text identifier.

    Returns:
        dict: Elasticsearch hits.
    """

    # Get the text id.
    text = Text.get(
        Text.corpus==corpus,
        Text.identifier==identifier,
    )

    # Get syllabi that assign the text.
    doc_ids = Citation_Index.docs_with_text(text.id)

    # Rank texts assigned by those sylalbi.
    ranks = Citation_Index.compute_ranking(dict(
        document_id=doc_ids
    ))

    # Omit the seed text.
    ranks.pop(str(text.id))

    # Materialize the text metadata.
    texts = Text_Index.materialize_ranking(ranks)

    return texts


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


def institution_facets():

    """
    Materialize institution facets with counts.

    Returns:
        dict: {label, value, count}
    """

    counts = Citation_Index.count_facets('institution_id')
    return Institution_Index.materialize_institution_facets(counts)


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


def load_indexes(mock=False):

    """
    Populate public-facing indexes.
    """

    for index in [
        Citation_Index,
        Text_Index,
        Subfield_Index,
        Field_Index,
        Institution_Index,
    ]:

        index.es_insert(mock=mock)
