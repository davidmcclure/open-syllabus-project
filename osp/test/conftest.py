

import pytest

from osp.common.config import config as _config
from osp.test.corpus.mock_osp import MockOSP
from osp.test.citations.hlom.mock_hlom import MockHLOM
from osp.api.server import app

from osp.citations.hlom.index import HLOMIndex
from osp.corpus.index import CorpusIndex
from osp.corpus.models.document import Document
from osp.corpus.models.format import Document_Format
from osp.corpus.models.text import Document_Text

from osp.dates.models.archive_url import Document_Date_Archive_Url
from osp.dates.models.file_metadata import Document_Date_File_Metadata
from osp.dates.models.semester import Document_Date_Semester

from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation

from playhouse.test_utils import test_database


@pytest.fixture(scope='session', autouse=True)
def test_env():

    """
    Merge the testing parameters into the configuration.
    """

    _config.paths.append('/etc/osp/osp.test.yml')
    _config.read()


@pytest.yield_fixture
def config():

    """
    Reset the configuration object after each test.

    Yields:
        The modify-able config object.
    """

    yield _config
    _config.read()


@pytest.yield_fixture
def mock_osp(config):

    """
    Provide a MockOSP instance, and automatically point the configuration
    object at the path of the mock corpus.

    Args:
        config (Config)

    Yields:
        MockOSP
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
def mock_hlom(config):

    """
    Provide a MockHLOM instance, and automatically point the configuration
    object at the path of the mock corpus.

    Args:
        config (Config)

    Yields:
        MockHLOM
    """

    hlom = MockHLOM()

    # Point config -> mock.
    config.config.update_w_merge({
        'hlom': {
            'corpus': hlom.path
        }
    })

    yield hlom
    hlom.teardown()


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
        Document_Date_File_Metadata,
        HLOM_Record,
        HLOM_Citation,
    ]

    with test_database(config.get_db(), tables):
        yield


@pytest.yield_fixture
def queue(config):

    """
    Clear the RQ queue.

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
    index.reset()

    yield index


@pytest.yield_fixture
def hlom_index(config):

    """
    Clear the HLOM index.
    """

    index = HLOMIndex()
    index.reset()

    yield index
