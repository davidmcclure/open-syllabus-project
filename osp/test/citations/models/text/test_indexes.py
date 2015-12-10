

import pytest

from osp.citations.models import Text
from peewee import IntegrityError


def test_unique_identifier(models, add_text):

    """
    Don't allow duplicate identifiers.
    """

    add_text(identifier='000')

    with pytest.raises(IntegrityError):
        add_text(identifier='000')
