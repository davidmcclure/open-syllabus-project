

import pytest

from osp.corpus.models.document import Document as _Document
from osp.common.config import config
from playhouse.test_utils import test_database
from contextlib import contextmanager


@contextmanager
def db(model):

    """
    Assign a model to the testing database.

    Args:
        model (peewee.Model): The model under test.

    Yields:
        A context with the wrapped model.
    """

    with test_database(config.get_db('test'), [model]):
        yield


@pytest.yield_fixture
def Document():
    with db(_Document): yield _Document
