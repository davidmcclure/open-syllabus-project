

import pytest

from osp.citations.utils import tokenize_field
from osp.citations.models import Text


@pytest.mark.parametrize('surname,is_toponym', [
    ('Alabama', True),
    ('Canada', True),
    ('War and Peace', False),
])
def test_surname_is_toponym(surname, is_toponym):

    text = Text(surname=surname)

    assert text.surname_is_toponym() == is_toponym
