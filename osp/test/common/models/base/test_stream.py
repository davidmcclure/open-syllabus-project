

import pytest

from osp.citations.models import Text


pytestmark = pytest.mark.usefixtures('db')


def test_stream(add_text):

    """
    BaseModel.stream() should generate all records in the table.
    """

    for i in range(100):
        add_text()

    ids = []
    for row in Text.stream(10):
        ids.append(row.id)

        # Possible to save, since we're not in a transaction.
        row.save()

    assert ids == list(range(1, 101))
