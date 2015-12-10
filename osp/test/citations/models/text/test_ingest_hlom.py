

import pytest
import uuid

from osp.citations.models import Text


def test_load_rows(models, mock_hlom):

    """
    Text.ingest_hlom() should ingest HLOM MARC records.
    """

    records = []

    # 10 segments, each with 10 records.
    for i in range(10):
        for j in range(10):

            cn = str(uuid.uuid4())

            records.append(mock_hlom.add_marc(

                data_file = str(i),
                control_number = cn,

                title       = 't'+cn,
                author      = 'a'+cn,
                publisher   = 'p'+cn,
                pubyear     = 'd'+cn,

            ))

    Text.ingest_hlom()

    # Should ingest 100 records.
    assert Text.select().count() == 100

    for r in records:

        cn = r.control_number()

        assert Text.select().where(
            Text.identifier == cn,
            Text.title      == 't'+cn,
            Text.author     == 'a'+cn,
            Text.publisher  == 'p'+cn,
            Text.date       == 'd'+cn,
        )


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
