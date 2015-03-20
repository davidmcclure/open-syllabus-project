

from osp.corpus.utils import html_text


def test_extract_text(mock_osp):

    """
    Text inside HTML tags should be extracted.
    """

    html = '<p>text</p>'

    path = mock_osp.add_file(content=html, ftype='html')
    text = html_text(path)
    assert text == 'text'


def test_ignore_scripts_and_styles(mock_osp):

    """
    By default, <script> and <style> tags should be ignored.
    """

    html = """
    <style>style</style>
    <script>script</script>
    <p>text</p>
    """

    path = mock_osp.add_file(content=html, ftype='html')
    text = html_text(path).strip()
    assert text == 'text'


def test_ignore_custom_tags(mock_osp):

    """
    Tags explicitly passed in `excluded` should be ignored.
    """

    html = """
    <h1>h1</h1>
    <h2>h2</h2>
    <h3>h3</h3>
    """

    path = mock_osp.add_file(content=html, ftype='html')
    text = html_text(path, ['h1', 'h2']).strip()
    assert text == 'h3'
