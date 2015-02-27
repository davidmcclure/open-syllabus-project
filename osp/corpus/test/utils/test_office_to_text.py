

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

    # Create a .docx.
    path = corpus.add_file('000', 'text', 'docx')

    # Should extract the text.
    text = office_to_text(path).strip()
    assert text == 'text'
