

import pytest

from osp.citations.models import Text
from peewee import IntegrityError


def test_unique_corpus_identifier(add_text):

    """
    Don't allow duplicate corpus+identifier.
    """

    add_text(corpus='jstor', identifier='001')

    with pytest.raises(IntegrityError):
        add_text(corpus='jstor', identifier='001')
