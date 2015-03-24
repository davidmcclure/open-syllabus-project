

import pytest

from osp.corpus.models.document import Document
from osp.corpus.models.text import Document_Text
from peewee import IntegrityError


def test_unique_paths(models):

    """
    The `document` column should be unique.
    """

    doc = Document.create(path='path')
    Document_Text.create(document=doc, text='text')

    with pytest.raises(IntegrityError):
        Document_Text.create(document=doc, text='text')
