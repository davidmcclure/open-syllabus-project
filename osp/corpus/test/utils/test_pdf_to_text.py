

import pytest

from osp.corpus.test.mocks.corpus import MockCorpus
from osp.corpus.utils import pdf_to_text


def test_extract_text():

    """
    Text in pages should be extracted and concatenated.
    """

    corpus = MockCorpus()
    corpus.add_segment('000')

    # Create a PDF with 3 pages.
    handle = corpus.add_file('000', 'text', 'pdf')

    # Should extract the text.
    text = pdf_to_text(handle.name).strip()
    assert text == 'text'
