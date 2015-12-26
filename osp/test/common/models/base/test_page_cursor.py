

import pytest

from osp.citations.models import Text


def test_page_cursor(db, add_text):

    """
    BaseModel.page_cursor() should generate record instances in an id-ordered
    "page", defined by a page count and 0-based index.
    """

    for i in range(1000):
        add_text()

    ids = []
    for i in range(7):
        for text in Text.page_cursor(7, i):
            ids.append(text.id)

    assert list(ids) == list(range(1, 1001))
