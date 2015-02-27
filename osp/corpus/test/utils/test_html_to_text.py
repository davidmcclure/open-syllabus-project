

import pytest

from osp.corpus.utils import html_to_text
from osp.corpus.test.mocks.corpus import MockCorpus


@pytest.fixture
def corpus():
    return MockCorpus()


def test_extract_text(corpus):

    """
    Text inside HTML tags should be extracted.
    """

    path = corpus.add_file('<p>text</p>')
    text = html_to_text(path)
    assert text == 'text'


def test_ignore_scripts_and_styles(corpus):

    """
    By default, <script> and <style> tags should be ignored.
    """

    html = """
    <style>style</style>
    <script>script</script>
    <p>text</p>
    """

    path = corpus.add_file(html)
    text = html_to_text(path).strip()
    assert text == 'text'


def test_ignore_custom_tags(corpus):

    """
    Tags explicitly passed in `excluded` should be ignored.
    """

    html = """
    <h1>h1</h1>
    <h2>h2</h2>
    <h3>h3</h3>
    """

    path = corpus.add_file(html)
    text = html_to_text(path, ['h1', 'h2']).strip()
    assert text == 'h3'
