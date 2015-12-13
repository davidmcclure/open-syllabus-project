

import pytest
import uuid

from osp.citations.models import Text


def test_set_corpus(models, mock_hlom):

    mock_hlom.add_marc()
    Text.ingest_hlom()

    assert Text.select().first().corpus == 'hlom'


def test_set_identifier(models, mock_hlom):

    mock_hlom.add_marc(control_number='001')
    Text.ingest_hlom()

    assert Text.select().first().identifier == '001'


def test_set_title(models, mock_hlom):

    mock_hlom.add_marc(title='Book Title')
    Text.ingest_hlom()

    assert Text.select().first().title == 'Book Title'


def test_set_author(models, mock_hlom):

    mock_hlom.add_marc(author='David W. McClure')
    Text.ingest_hlom()

    assert Text.select().first().author == ['David W. McClure']


def test_set_publisher(models, mock_hlom):

    mock_hlom.add_marc(publisher='Chicago Press')
    Text.ingest_hlom()

    assert Text.select().first().publisher == 'Chicago Press'


def test_set_date(models, mock_hlom):

    mock_hlom.add_marc(pubyear='1987')
    Text.ingest_hlom()

    assert Text.select().first().date == '1987'


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

                title       = 'title'+cn,
                author      = 'author'+cn,
                publisher   = 'publisher'+cn,
                pubyear     = 'pubyear'+cn,

            ))

    Text.ingest_hlom()

    # Should ingest 100 records.
    assert Text.select().count() == 100

    for r in records:

        cn = r.control_number()

        assert Text.select().where(

            Text.corpus     == 'hlom',
            Text.identifier == cn,

            Text.author.contains('author'+cn),

            Text.title      == 'title'+cn,
            Text.publisher  == 'publisher'+cn,
            Text.date       == 'pubyear'+cn,

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
