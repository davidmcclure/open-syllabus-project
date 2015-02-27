

import pytest

from osp.corpus.utils import tika_is_online, office_to_text


pytestmark = pytest.mark.skipif(
    tika_is_online() == False,
    reason='Tika is offline.'
)


def test_extract_text(corpus):

    """
    Text should be extracted via Tika.
    """

    # Create a .docx.
    path = corpus.add_file(content='text', ftype='docx')

    # Should extract the text.
    text = office_to_text(path).strip()
    assert text == 'text'
