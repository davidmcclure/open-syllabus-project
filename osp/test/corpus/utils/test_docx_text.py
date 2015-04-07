

from osp.corpus.utils import docx_text
from osp.test.utils import requires_tika


@requires_tika
def test_extract_text(mock_osp):

    """
    Text should be extracted via Tika.
    """

    # Create a .docx.
    path = mock_osp.add_file(content='text', ftype='docx')

    # Should extract the text.
    text = docx_text(path).strip()
    assert text == 'text'
