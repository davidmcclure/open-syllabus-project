

import pytest

from osp.test.corpus.mocks.corpus import MockCorpus


@pytest.fixture
def mock_corpus(request):

    corpus = MockCorpus()

    def teardown():
        corpus.teardown()

    request.addfinalizer(teardown)
    return corpus
