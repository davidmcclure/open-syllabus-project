

import pytest

from osp.corpus.test.markers import requires_tika
from osp.corpus.utils import office_to_text


@requires_tika
def test_extract_text(corpus):

    """
    Text should be extracted via Tika.
    """

    # Create a .docx.
    path = corpus.add_file(content='text', ftype='docx')

    # Should extract the text.
    text = office_to_text(path).strip()
    assert text == 'text'
