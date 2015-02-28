

import pytest

from osp.corpus.test.mocks.corpus import MockCorpus


@pytest.fixture
def mock_corpus():
    return MockCorpus()
