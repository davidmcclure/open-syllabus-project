

import pytest

from osp.corpus.models.document import Document
from osp.dates.models.archive_url import Document_Date_Archive_Url
from osp.dates.jobs.ext_archive_url import date_format, ext_archive_url
from datetime import datetime
from dateutil.relativedelta import relativedelta


@pytest.fixture()
def ext(models, mock_corpus):

    """
    Provide a function that mocks a file with a given URL and returns a
    document instance bound to the new path.

    Returns:
        function: A helper that mocks a file with the provided URL, runs the
        job, and returns the new `document_date_archive_url` row.
    """

    def _ext(url):

        # Create a document.
        path = mock_corpus.add_file(log={'url': url})
        document = Document.create(path=path)

        # Extract the date.
        ext_archive_url(document.id)

        # Pop out the new row.
        return (
            Document_Date_Archive_Url
            .select()
            .where(Document_Date_Archive_Url.document==document)
            .first()
        )

    return _ext


def test_archive_url(ext):

    """
    ext_archive_url() should extract a timestamp from an Internet Archive URL.
    """

    url1 = 'https://web.archive.org/web/20150102030405'
    url2 = 'http://yale.edu/syllabus.html'

    row = ext(url1+'/'+url2)

    assert row.date.year    == 2015
    assert row.date.month   == 1
    assert row.date.day     == 2
    assert row.date.hour    == 3
    assert row.date.minute  == 4
    assert row.date.second  == 5


def test_ignore_future_timestamp(ext):

    """
    Don't index timestamps from the future.
    """

    # Get now + 1 year.
    future = datetime.now() + relativedelta(years=1)
    timestamp = future.strftime(date_format)

    url1 = 'https://web.archive.org/web/'+timestamp
    url2 = 'http://yale.edu/syllabus.html'

    row = ext(url1+'/'+url2)

    # Shouldn't write a row.
    assert Document_Date_Archive_Url.select().count() == 0


def test_ignore_regular_url(ext):

    """
    When the syllabus was scraped from a regular URL, don't write a row.
    """

    row = ext('http://yale.edu/syllabus.html')

    # Shouldn't write a row.
    assert Document_Date_Archive_Url.select().count() == 0
