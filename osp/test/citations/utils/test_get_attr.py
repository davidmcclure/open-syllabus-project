

import pytest

from osp.citations.utils import get_attr
from bs4 import BeautifulSoup


@pytest.mark.parametrize('tag,value', [

    ('<tag attr="value" />', 'value'),

    # Strip whitespace.
    ('<tag attr="  value  " />', 'value'),

    # Empty value -> None.
    ('<tag attr="" />', None),
    ('<tag attr="  " />', None),

    # Missing attr -> None.
    ('<tag />', None),

    # Missing tag -> None.
    ('', None),

])
def test_get_text(tag, value):
    tree = BeautifulSoup(tag, 'lxml')
    assert get_attr(tree, 'tag', 'attr') == value
