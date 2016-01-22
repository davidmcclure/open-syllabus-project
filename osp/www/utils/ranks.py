

from osp.citations.models import Text_Index
from osp.citations.models import Citation_Index

from osp.common import config
from osp.www.cache import cache


@cache.memoize(unless=config.is_test)
def rank_texts(filters={}, query=None, size=1000):

    """
    Filter and rank texts.

    Args:
        filters (dict): Citation metadata filters.
        query (str): A text metadata search query.

    Returns:
        dict: Elasticsearch hits.
    """

    # Filter citation counts, if non-empty filters.
    if any(filters.values()):
        ranks = Citation_Index.compute_ranking(filters)

    else:
        ranks = None

    # Materialize the text metadata.
    texts = Text_Index.materialize_ranking(ranks, query, size)

    return texts


@cache.memoize(unless=config.is_test)
def assigned_with(text_id, size=200):

    """
    Given a "seed" text, rank other texts assigned on the same syllabi.

    Args:
        text_id (int): The text id.

    Returns:
        dict: Elasticsearch hits.
    """

    # Get syllabi that assign the text.
    doc_ids = Citation_Index.docs_with_text(text_id)

    # Rank texts assigned by those sylalbi.
    ranks = Citation_Index.compute_ranking(dict(
        document_id=doc_ids
    ))

    # Omit the seed text.
    ranks.pop(str(text_id))

    # Materialize the text metadata.
    texts = Text_Index.materialize_ranking(ranks, size=size)

    return texts
