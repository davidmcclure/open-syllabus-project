

import pytest

from osp.citations.models import Citation


pytestmark = pytest.mark.usefixtures('db')


def test_stream(add_citation):

    """
    BaseModel.stream() should generate all records in the table.
    """

    for i in range(100):
        add_citation()

    ids = []
    for row in Citation.stream(10):

        ids.append(row.id)

        # Possible to save, since we're not in a transaction.
        row.valid = False
        row.save()

    assert ids == list(range(1, 101))
