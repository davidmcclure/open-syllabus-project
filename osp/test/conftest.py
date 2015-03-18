

import pytest

from osp.common.config import config as _config
from osp.common.models.base import queue as _queue

from osp.api.server import app
from osp.test.corpus.mocks.corpus import MockCorpus
from contextlib import contextmanager
from playhouse.test_utils import test_database
from redis import StrictRedis

from osp.corpus.models.document import Document
from osp.corpus.models.format import Document_Format
from osp.corpus.models.text import Document_Text
from osp.dates.models.archive_url import Document_Date_Archive_Url
from osp.dates.models.file_metadata import Document_Date_File_Metadata
from osp.dates.models.semester import Document_Date_Semester


@pytest.yield_fixture
def config():

    """
    Provide a config object. When the test finishes, restore the original
    values loaded from the YAML files, which makes it possible to modify the
    config without changing state across tests.

    Yields:
        The modify-able config object.
    """

    yield _config
    _config.read()


@pytest.yield_fixture
def mock_corpus(config):

    """
    Provide a MockCorpus instance, and automatically point the configuration
    object at the path of the mock corpus.

    Args:
        config (Config)

    Yields:
        MockCorpus
    """

    corpus = MockCorpus()

    # Point config -> mock.
    config.config.update_w_merge({
        'osp': {
            'corpus': corpus.path
        }
    })

    yield corpus
    corpus.teardown()


@pytest.yield_fixture
def models():

    """
    Assign models to the testing database.

    Yields:
        A context with the wrapped model.
    """

    tables = [
        Document,
        Document_Format,
        Document_Text,
        Document_Date_Archive_Url,
        Document_Date_Semester,
        Document_Date_File_Metadata
    ]

    with test_database(_config.get_db('test'), tables):
        yield


@pytest.yield_fixture
def queue():

    """
    Point the queue at a testing Redis database.

    Yields:
        The RQ queue.
    """

    old = _queue.connection
    new = StrictRedis(db=1)
    _queue.connection = new

    yield _queue

    new.flushdb()
    _queue.connection = old


@pytest.yield_fixture
def api_client():

    """
    Get a test client for the worker API.

    Yields:
        The test client.
    """

    app.testing = True
    yield app.test_client()
