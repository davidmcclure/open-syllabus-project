

import pytest

from osp.corpus.models.document import Document
from peewee import IntegrityError


def test_unique_paths(models):

    """
    The `path` column on the document table should be unique.
    """

    Document.create(path='path')

    with pytest.raises(IntegrityError):
        Document.create(path='path')
