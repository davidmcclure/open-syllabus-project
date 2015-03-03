

import pytest

from osp.test.corpus.markers import requires_tika
from osp.corpus.utils import office_to_text


@requires_tika
def test_extract_text(mock_corpus):

    """
    Text should be extracted via Tika.
    """

    # Create a .docx.
    path = mock_corpus.add_file(content='text', ftype='docx')

    # Should extract the text.
    text = office_to_text(path).strip()
    assert text == 'text'
