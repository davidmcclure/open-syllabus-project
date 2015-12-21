

from osp.citations.models import Citation_Index
from osp.citations.models import Text
from osp.citations.models import Text_Index
from osp.institutions.models import Institution_Index
from osp.fields.models import Field_Index
from osp.fields.models import Subfield_Index


def rank_texts(filters={}, query=None):

    """
    Filter and rank texts.
    """

    # Filter and rank the texts.
    ranks = Citation_Index.rank_texts(filters)

    # Materialize the text metadata.
    texts = Text_Index.materialize_ranking(ranks, query)

    return texts


def assigned_with(corpus, identifier):

    """
    Given a "seed" text, rank other texts assigned on the same syllabi.
    """

    # Get the text id.
    text = Text.get(
        Text.corpus==corpus,
        Text.identifier==identifier,
    )

    # Get documents that assign the text.
    doc_ids = Citation_Index.docs_with_text(text.id)

    # Rank texts assigned on those docs.
    ranks = Citation_Index.rank_texts(dict(
        document_id=doc_ids
    ))

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
