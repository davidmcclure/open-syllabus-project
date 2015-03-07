

from osp.corpus.models.document import Document
from osp.dates.models.archive_url import Document_Date_Archive_Url
from osp.dates.jobs.archive_url import archive_url


def test_timestamp_exists(models, mock_corpus):

    """
    archive_url() should write the IA URL timestamp, when one exists.
    """

    url1 = 'https://web.archive.org/web/20031119022539'
    url2 = 'http:/ce.byu.edu/is/ahtg/sec11/l19.htm'

    # Mock an Internet Archive URL.
    path = mock_corpus.add_file(log={'url': url1+'/'+url2 })
    document = Document.create(path=path)

    # Write the timestamp.
    archive_url(document.id)

    # Pop out the new row.
    row = Document_Date_Archive_Url.get(
        Document_Date_Archive_Url.document==document
    )

    assert row.timestamp == '20031119022539'
