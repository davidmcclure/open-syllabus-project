

import pytest

from osp.citations.models import Text


pytestmark = pytest.mark.usefixtures('db')


def test_set_corpus(mock_jstor):

    mock_jstor.add_article()
    Text.ingest_jstor()

    assert Text.select().first().corpus == 'jstor'


def test_set_identifier(mock_jstor):

    mock_jstor.add_article(article_id='001')
    Text.ingest_jstor()

    assert Text.select().first().identifier == '001'


def test_set_title(mock_jstor):

    mock_jstor.add_article(article_title='Article Title')
    Text.ingest_jstor()

    assert Text.select().first().title == 'Article Title'


def test_set_single_author(mock_jstor):

    mock_jstor.add_article(author=[('David W.', 'McClure')])
    Text.ingest_jstor()

    assert Text.select().first().authors == ['McClure, David W.']


def test_set_multiple_authors(mock_jstor):

    mock_jstor.add_article(author=[
        ('David W.', 'McClure'),
        ('Kara G.', 'Weisman'),
    ])

    Text.ingest_jstor()

    assert Text.select().first().authors == [
        'McClure, David W.',
        'Weisman, Kara G.',
    ]


def test_set_publisher(mock_jstor):

    mock_jstor.add_article(publisher_name='Chicago Journals')
    Text.ingest_jstor()

    assert Text.select().first().publisher == 'Chicago Journals'


def test_set_date(mock_jstor):

    mock_jstor.add_article(pub_year=1987, pub_month=6, pub_day=25)
    Text.ingest_jstor()

    assert Text.select().first().date == '1987-06-25'


def test_set_journal_title(mock_jstor):

    mock_jstor.add_article(journal_title='Critical Inquiry')
    Text.ingest_jstor()

    assert Text.select().first().journal_title == 'Critical Inquiry'


def test_set_journal_identifier(mock_jstor):

    mock_jstor.add_article(journal_id='criticalinquiry')
    Text.ingest_jstor()

    assert Text.select().first().journal_identifier == 'criticalinquiry'


def test_set_issue_volume(mock_jstor):

    mock_jstor.add_article(issue_volume=200)
    Text.ingest_jstor()

    assert Text.select().first().issue_volume == '200'


def test_set_issue_number(mock_jstor):

    mock_jstor.add_article(issue_number=10)
    Text.ingest_jstor()

    assert Text.select().first().issue_number == '10'


def test_set_pagination(mock_jstor):

    mock_jstor.add_article(fpage=200, lpage=300)
    Text.ingest_jstor()

    assert Text.select().first().pagination == '200-300'


def test_set_url(mock_jstor):

    mock_jstor.add_article(url='http://test.org')
    Text.ingest_jstor()

    assert Text.select().first().url == 'http://test.org'


def test_load_multiple(mock_jstor):

    """
    Text.ingest_jstor() should ingest multiple records.
    """

    # 100 records.
    for i in range(100):
        mock_jstor.add_article()

    Text.ingest_jstor()

    # 100 rows.
    assert Text.select().count() == 100


@pytest.mark.parametrize('title,author', [

    # Empty author.
    ('title', [('', '')]),

    # Empty title.
    ('', [('David W.', 'McClure')]),

])
def test_require_title_and_author(title, author, mock_jstor):

    """
    Skip records that don't have a query-able title and author.
    """

    mock_jstor.add_article(article_title=title, author=author)
    Text.ingest_jstor()

    assert Text.select().count() == 0
