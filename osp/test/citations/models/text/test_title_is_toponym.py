

import pytest

from osp.citations.utils import tokenize_field
from osp.citations.models import Text


@pytest.mark.parametrize('title,is_toponym', [
    ('Alabama', True),
    ('Canada', True),
    ('War and Peace', False),
])
def test_title_is_toponym(title, is_toponym):

    text = Text(title=title)

    assert text.title_is_toponym() == is_toponym
