

import pytest

from osp.corpus.utils import tika_is_online, office_to_text
from osp.corpus.test.mocks.corpus import MockCorpus


pytestmark = pytest.mark.skipif(
    tika_is_online() == False,
    reason='Tika is offline.'
)


def test_extract_text():

    """
    Text should be extracted via Tika.
    """

    corpus = MockCorpus()
    corpus.add_segment('000')

    # Create a .docx.
    handle = corpus.add_docx('000', 'docx', 'text')

    # Should extract the text.
    text = office_to_text(handle.read())
    assert text.strip() == 'text'
