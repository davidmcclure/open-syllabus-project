

import pytest

from osp.corpus.models.document import Document as _Document
from osp.common.config import config as _config
from osp.test.corpus.mocks.corpus import MockCorpus
from playhouse.test_utils import test_database
from contextlib import contextmanager


@pytest.fixture
def config(request):

    """
    Provide a config object. When the test finishes, restore the original
    values loaded from the YAML files, which makes it possible to modify the
    config without changing state across tests.

    Args:
        request (FixtureRequest)

    Returns:
        The modify-able config object.
    """

    def teardown():
        _config.reset()

    request.addfinalizer(teardown)
    return _config


@pytest.fixture
def mock_corpus(request, config):

    """
    Provide a MockCorpus instance, and automatically point the configuration
    object at the path of the mock corpus.

    Args:
        request (FixtureRequest)
        config (Config)

    Returns:
        MockCorpus
    """

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
