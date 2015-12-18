

import pytest

from osp.fields.models import Subfield_Document
from peewee import IntegrityError


def test_unique_pairs(add_subfield, add_doc):

    """
    Don't allow duplicate links between the same field -> document.
    """

    s = add_subfield()
    d = add_doc()

    Subfield_Document.create(
        subfield=s,
        document=d,
        offset=1,
        snippet='abc'
    )

    with pytest.raises(IntegrityError):

        Subfield_Document.create(
            subfield=s,
            document=d,
            offset=2,
            snippet='def'
        )
