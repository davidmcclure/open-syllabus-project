

import pytest

from osp.corpus.test.mocks.corpus import MockCorpus
from osp.corpus.utils import pdf_to_text


def test_extract_text():
    """
    Text in pages should be extracted and concatenated.
    """
    corpus = MockCorpus()
    corpus.add_segment('000')
    handle = corpus.add_pdf('000', 'pdf', ['p1', 'p2', 'p3'])
    text = pdf_to_text(handle.name)

    assert text.split() == ['p1', 'p2', 'p3']
