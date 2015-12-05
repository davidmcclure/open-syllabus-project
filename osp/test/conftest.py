

import pytest

# Globals:
from osp.api.server import app
from osp.common.config import config as _config

# Models:
from osp.corpus.models.document import Document
from osp.corpus.models.format import Document_Format
from osp.corpus.models.text import Document_Text
from osp.dates.models.archive_url import Document_Date_Archive_Url
from osp.dates.models.semester import Document_Date_Semester
from osp.dates.models.file_metadata import Document_Date_File_Metadata
from osp.institutions.models.institution import Institution
from osp.hlom.models.record import HLOM_Record
from osp.hlom.models.citation import HLOM_Citation
from osp.fields.models.field import Field
from osp.fields.models.field_document import Field_Document

# Helpers:
from playhouse.test_utils import test_database
from osp.test.corpus.mock_osp import MockOSP
from osp.test.hlom.mock_hlom import MockHLOM


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
        Institution,
        HLOM_Record,
        HLOM_Citation,
        Field,
        Field_Document,
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

    config.rq.connection.flushdb()
    yield config.rq


@pytest.yield_fixture
def api_client():

    """
    Get a test client for the worker API.

    Yields:
        The test client.
    """

    app.testing = True
    yield app.test_client()


@pytest.fixture
def requires_es(config):

    """
    Require Elasticsearch.
    """

    if not config.es.ping():
        pytest.skip('Elasticsearch offline.')


@pytest.fixture
def corpus_index(requires_es):

    """
    Clear the corpus index.
    """

    Document_Text.es_reset()


@pytest.fixture
def hlom_index(requires_es):

    """
    Clear the HLOM index.
    """

    HLOM_Record.es_reset()
