

import pytest

from osp.corpus.test.mocks.corpus import MockCorpus
from osp.corpus.utils import pdf_to_text


@pytest.fixture
def corpus():
    return MockCorpus()


def test_extract_text(corpus):

    """
    Text in pages should be extracted and concatenated.
    """

    # Create a PDF with 3 pages.
    path = corpus.add_file('text', ftype='pdf')

    # Should extract the text.
    text = pdf_to_text(path).strip()
    assert text == 'text'
