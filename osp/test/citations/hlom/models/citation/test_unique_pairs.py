

import pytest

from osp.corpus.models.document import Document
from peewee import IntegrityError


def test_unique_pairs(models):

    """
    Don't allow duplicate links between the same text -> syllabus pair.
    """

    pass
