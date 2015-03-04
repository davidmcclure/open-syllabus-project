

import pytest

from peewee import IntegrityError


def test_unique_paths(Document):

    """
    The `path` column on the document table should be unique.
    """

    Document.create(path='path')

    with pytest.raises(IntegrityError):
        Document.create(path='path')
