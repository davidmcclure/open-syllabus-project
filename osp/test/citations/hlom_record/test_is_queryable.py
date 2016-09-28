

import pytest

from osp.citations.hlom_record import HLOM_Record


@pytest.mark.parametrize('title,author,queryable', [

    # Title and author.
    ('Book Title', 'McClure, David W.', True),

    # Missing title.
    ('', 'McClure, David W.', False),
    ('  ', 'McClure, David W.', False),
    ('00', 'McClure, David W.', False),

    # Missing author.
    ('Book Title', '', False),
    ('Book Title', '  ', False),
    ('Book Title', '00', False),

    # Missing title and author.
    ('', '', False),
    ('  ', '  ', False),
    ('00', '00', False),

])
def test_is_queryable(title, author, queryable, mock_hlom):

    record = mock_hlom.add_marc(title=title, author=author)

    assert HLOM_Record(record).is_queryable() == queryable
