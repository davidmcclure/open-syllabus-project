

from osp.corpus.utils import html_to_text


def test_extract_text():
    """
    Text inside HTML tags should be extracted.
    """
    assert html_to_text('<p>text</p>') == 'text'


def test_ignore_scripts_and_styles():
    """
    By default, <script> and <style> tags should be ignored.
    """
    html = """
    <style>style</style>
    <script>script</script>
    <p>text</p>
    """

    assert html_to_text(html).strip() == 'text'


def test_ignore_custom_tags():
    """
    Tags explicitly passed in `excluded` should be ignored.
    """
    html = """
    <h1>h1</h1>
    <h2>h2</h2>
    <h3>h3</h3>
    """

    text = html_to_text(html, ['h1', 'h2'])
    assert text.strip() == 'h3'
