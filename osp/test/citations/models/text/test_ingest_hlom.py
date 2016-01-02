

import pytest
import uuid

from osp.citations.models import Text


pytestmark = pytest.mark.usefixtures('db')


def test_set_corpus(mock_hlom):

    mock_hlom.add_marc()
    Text.ingest_hlom()

    assert Text.select().first().corpus == 'hlom'


def test_set_identifier(mock_hlom):

    mock_hlom.add_marc(control_number='001')
    Text.ingest_hlom()

    assert Text.select().first().identifier == '001'


def test_set_title(mock_hlom):

    mock_hlom.add_marc(title='Book Title')
    Text.ingest_hlom()

    assert Text.select().first().title == 'Book Title'


def test_set_author(mock_hlom):

    mock_hlom.add_marc(author='David W. McClure')
    Text.ingest_hlom()

    assert Text.select().first().authors == ['David W. McClure']


def test_set_publisher(mock_hlom):

    mock_hlom.add_marc(publisher='Chicago Press')
    Text.ingest_hlom()

    assert Text.select().first().publisher == 'Chicago Press'


def test_set_date(mock_hlom):

    mock_hlom.add_marc(pubyear='1987')
    Text.ingest_hlom()

    assert Text.select().first().date == '1987'


def test_load_multiple(mock_hlom):

    """
    Text.ingest_hlom() should ingest multiple records.
    """

    # 100 records.
    for i in range(100):
        mock_hlom.add_marc()

    Text.ingest_hlom()

    # 100 rows.
    assert Text.select().count() == 100


@pytest.mark.parametrize('title,author', [

    # Empty author.
    ('title', ''),
    ('title', '  '),
    ('title', '00'),

    # Empty title.
    ('', 'author'),
    ('  ', 'author'),
    ('00', 'author'),

    # Both empty.
    ('', ''),
    ('  ', '  '),
    ('00', '00'),

])
def test_require_title_and_author(title, author, mock_hlom):

    """
    Skip records that don't have a query-able title and author.
    """

    mock_hlom.add_marc(title=title, author=author)
    Text.ingest_hlom()

    assert Text.select().count() == 0
