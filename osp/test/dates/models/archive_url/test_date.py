

from osp.dates.models.archive_url import Document_Date_Archive_Url


def test_date(models):

    """
    Document_Date_Archive_Url#date should convert the URL timestamp into a
    regular datetime instance.
    """

    row = Document_Date_Archive_Url(timestamp='20150102030405')

    assert row.date.year    == 2015
    assert row.date.month   == 1
    assert row.date.day     == 2
    assert row.date.hour    == 3
    assert row.date.minute  == 4
    assert row.date.second  == 5
