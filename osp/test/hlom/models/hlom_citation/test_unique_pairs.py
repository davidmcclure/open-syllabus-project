

import pytest

from osp.hlom.models import HLOM_Citation
from peewee import IntegrityError


def test_unique_pairs(models, add_hlom, add_doc):

    """
    Don't allow duplicate links between the same text -> syllabus pair.
    """

    d = add_doc()
    r = add_hlom()

    HLOM_Citation.create(document=d, record=r)

    with pytest.raises(IntegrityError):
        HLOM_Citation.create(document=d, record=r)
