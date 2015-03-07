

from osp.dates.models.archive_url import Document_Date_Archive_Url


def test_date():

    """
    Document_Date_Archive_Url#date should convert the raw Internet Archive
    timestamp into a regular datetime instance.
    """

    row = Document_Date_Archive_Url(timestamp='20031119022539')
    date = row.date

    assert date.tm_year == 2003
    assert date.tm_mon == 11
    assert date.tm_mday == 19
    assert date.tm_hour == 2
    assert date.tm_min == 25
    assert date.tm_sec == 39
