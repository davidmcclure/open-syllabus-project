

import pytest

from osp.corpus.syllabus import Syllabus
from osp.corpus.test.mocks.corpus import MockCorpus


@pytest.fixture
def corpus():
    return MockCorpus()


def test_file_name(corpus):
    pass
