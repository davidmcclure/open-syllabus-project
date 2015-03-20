

import pytest

from osp.common.config import config as _config
from osp.test.corpus.mock_osp import MockOSP
from osp.api.server import app

from osp.corpus.index import CorpusIndex
from osp.corpus.models.document import Document
from osp.corpus.models.format import Document_Format
from osp.corpus.models.text import Document_Text

from osp.dates.models.archive_url import Document_Date_Archive_Url
from osp.dates.models.file_metadata import Document_Date_File_Metadata
from osp.dates.models.semester import Document_Date_Semester

from playhouse.test_utils import test_database


@pytest.yield_fixture
def config():

    """
    Merge the testing parameters into the configuration.

    Yields:
        The modify-able config object.
    """

    _config.read(['/etc/osp/osp.test.yml'])

    yield _config
    _config.read()


@pytest.yield_fixture
def mock_osp(config):

    """
    Provide a MockCorpus instance, and automatically point the configuration
    object at the path of the mock corpus.

    Args:
        config (Config)

    Yields:
        MockCorpus
    """

    osp = MockOSP()

    # Point config -> mock.
    config.config.update_w_merge({
        'osp': {
            'corpus': osp.path
        }
    })

    yield osp
    osp.teardown()


@pytest.yield_fixture
def models(config):

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

    with test_database(config.get_db(), tables):
        yield


@pytest.yield_fixture
def queue(config):

    """
    Point the queue at a testing Redis database.

    Yields:
        The RQ queue.
    """

    queue = config.get_rq()
    queue.connection.flushdb()
    yield queue


@pytest.yield_fixture
def api_client():

    """
    Get a test client for the worker API.

    Yields:
        The test client.
    """

    app.testing = True
    yield app.test_client()


@pytest.yield_fixture
def corpus_index(config):

    """
    Clear the corpus index.
    """

    index = CorpusIndex()
    index.delete()
    index.create()

    yield index
