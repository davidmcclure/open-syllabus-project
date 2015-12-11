

import pytest

from osp.citations.models import Citation
from peewee import IntegrityError


def test_unique_pairs(models, add_doc, add_text):

    """
    Don't allow duplicate links between the same text -> syllabus pair.
    """

    d = add_doc()
    t = add_text()

    Citation.create(document=d, text=t, min_freq=1)

    with pytest.raises(IntegrityError):
        Citation.create(document=d, text=t, min_freq=1)
