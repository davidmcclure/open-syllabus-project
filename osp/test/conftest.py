

import pytest

from osp.corpus.models.document import Document as _Document
from osp.common.config import config as _config
from osp.test.corpus.mocks.corpus import MockCorpus
from playhouse.test_utils import test_database
from contextlib import contextmanager


@pytest.fixture
def config(request):

    def teardown():
        _config.reset()

    request.addfinalizer(teardown)
    return _config


@pytest.fixture
def mock_corpus(request, config):

    corpus = MockCorpus()

    # Point config -> mock.
    config.config.update_w_merge({
        'osp': {
            'corpus': corpus.path
        }
    })

    def teardown():
        corpus.teardown()

    request.addfinalizer(teardown)
    return corpus


@contextmanager
def db(model):

    """
    Assign a model to the testing database.

    Args:
        model (peewee.Model): The model under test.

    Yields:
        A context with the wrapped model.
    """

    with test_database(_config.get_db('test'), [model]):
        yield


@pytest.yield_fixture
def Document():
    with db(_Document): yield _Document
