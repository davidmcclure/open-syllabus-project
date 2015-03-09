

from osp.corpus.models.document import Document
from osp.dates.models.archive_url import Document_Date_Archive_Url
from osp.dates.jobs.archive_url import archive_url


def test_internet_archive_url(models, mock_corpus):

    """
    archive_url() should extract a timestamp from and Internet Archive URL.
    """

    url1 = 'https://web.archive.org/web/20150102030405'
    url2 = 'http://yale.edu/syllabus.html'

    # Mock an Internet Archive URL.
    path = mock_corpus.add_file(log={'url': url1+'/'+url2})
    document = Document.create(path=path)

    # Write the timestamp.
    archive_url(document.id)

    # Pop out the new row.
    row = Document_Date_Archive_Url.get(
        Document_Date_Archive_Url.document==document
    )

    assert row.timestamp == '20150102030405'


def test_regular_url(models, mock_corpus):

    """
    When the syllabus was scraped from a regular URL, don't write a row.
    """

    # Mock a regular URL.
    path = mock_corpus.add_file(log={
        'url': 'http://yale.edu/syllabus.html'
    })

    # Write the timestamp.
    document = Document.create(path=path)
    archive_url(document.id)

    # Shouldn't write a row.
    assert Document_Date_Archive_Url.select().count() == 0
