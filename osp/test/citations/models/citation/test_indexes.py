

import pytest

from osp.citations.models import Citation
from peewee import IntegrityError


def test_unique_pairs(models, add_text, add_doc, add_citation):

    """
    Don't allow duplicate links between the same text -> syllabus pair.
    """

    t = add_text()
    d = add_doc()

    add_citation(text=t, document=d)

    with pytest.raises(IntegrityError):
        add_citation(text=t, document=d)
