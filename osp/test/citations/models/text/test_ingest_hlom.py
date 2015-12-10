

import pytest

from osp.citations.models import Text


def test_load_rows(models, mock_hlom):

    """
    Text.ingest_hlom() should ingest HLOM MARC records.
    """

    records = []

    # 10 segments, each with 10 records.
    for i in range(10):
        for j in range(10):
            marc = mock_hlom.add_marc(data_file=str(i))
            records.append(marc)

    Text.ingest_hlom()

    # Should insert 100 records.
    assert Text.select().count() == 100


@pytest.mark.parametrize('title,author', [

    # Empty title.
    ('title', ''),

    # Empty author.
    ('', 'author'),

    # Both empty.
    ('', ''),
    ('  ', '  '),
    ('00', '00'),

])
def test_require_title_and_author(title, author, models, mock_hlom):

    """
    Skip records that don't have a query-able title and author.
    """

    mock_hlom.add_marc(title=title, author=author)
    Text.ingest_hlom()

    assert Text.select().count() == 0
