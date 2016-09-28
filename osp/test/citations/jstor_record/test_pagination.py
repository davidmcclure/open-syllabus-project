

import pytest

from osp.citations.jstor_record import JSTOR_Record


@pytest.mark.parametrize('fpage,lpage,pagination', [

    # Both.
    (100, 200, '100-200'),

    # Just fpage.
    (100, '', '100'),

    # Just lpage.
    ('', 200, '200'),

    # Neither.
    ('', '', None),

])
def test_pagination(fpage, lpage, pagination, mock_jstor):

    path = mock_jstor.add_article(fpage=fpage, lpage=lpage)

    assert JSTOR_Record(path).pagination() == pagination
