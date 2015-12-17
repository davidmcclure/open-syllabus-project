

import pytest

from osp.citations.utils import get_text
from bs4 import BeautifulSoup


@pytest.mark.parametrize('tag,text', [

    ('<tag>Article Title</tag>', 'Article Title'),

    # Strip whitespace.
    ('<tag>  Article Title  </tag>', 'Article Title'),

    # Empty text -> None.
    ('<tag></tag>', None),
    ('<tag>  </tag>', None),

    # Missing tag -> None.
    ('', None),

])
def test_get_text(tag, text):
    tree = BeautifulSoup(tag, 'lxml')
    assert get_text(tree, 'tag') == text
