

from osp.dates.models.archive_url import Document_Date_Archive_Url


def test_date():

    """
    Document_Date_Archive_Url#date should convert the raw Internet Archive
    timestamp into a regular datetime instance.
    """

    row = Document_Date_Archive_Url(timestamp='20150102030405')
    date = row.date

    assert date.tm_year == 2015
    assert date.tm_mon  == 1
    assert date.tm_mday == 2
    assert date.tm_hour == 3
    assert date.tm_min  == 4
    assert date.tm_sec  == 5
