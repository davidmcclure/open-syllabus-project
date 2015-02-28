

import pytest

from osp.corpus.test.mocks.corpus import MockCorpus


@pytest.fixture
def corpus(request):

    corpus = MockCorpus()

    def teardown():
        corpus.teardown()

    request.addfinalizer(teardown)
    return corpus
