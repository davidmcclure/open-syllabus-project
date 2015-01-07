

from osp.corpus.models.text import Text


def document_texts():

    """
    Get the most recent document texts.
    """

    return (
        Text
        .select()
        .distinct([Text.document])
        .order_by(Text.document, Text.created.desc())
    )
