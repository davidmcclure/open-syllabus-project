

from osp.corpus.models.document import Document
from osp.dates.models.archive_url import Document_Date_Archive_Url
from osp.dates.jobs.ext_archive_url import ext_archive_url


def test_internet_archive_url(models, mock_corpus):

    """
    archive_url() should extract a timestamp from and Internet Archive URL.
    """

    url1 = 'https://web.archive.org/web/20150102030405'
    url2 = 'http://yale.edu/syllabus.html'

    # Internet Archive URL.
    path = mock_corpus.add_file(log={
        'url': url1+'/'+url2
    })

    # Write the timestamp.
    document = Document.create(path=path)
    ext_archive_url(document.id)

    # Pop out the new row.
    row = Document_Date_Archive_Url.get(
        Document_Date_Archive_Url.document==document
    )

    # Store the original string.
    assert row.timestamp == '20150102030405'

    # Store a Postgres timestamp.
    assert row.date.year    == 2015
    assert row.date.month   == 1
    assert row.date.day     == 2
    assert row.date.hour    == 3
    assert row.date.minute  == 4
    assert row.date.second  == 5


def test_regular_url(models, mock_corpus):

    """
    When the syllabus was scraped from a regular URL, don't write a row.
    """

    # Regular URL.
    path = mock_corpus.add_file(log={
        'url': 'http://yale.edu/syllabus.html'
    })

    # Write the timestamp.
    document = Document.create(path=path)
    ext_archive_url(document.id)

    # Shouldn't write a row.
    assert Document_Date_Archive_Url.select().count() == 0
