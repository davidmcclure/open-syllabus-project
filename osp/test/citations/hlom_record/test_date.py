

from osp.citations.hlom_record import HLOM_Record


def test_date(mock_hlom):

    record = mock_hlom.add_marc(pubyear='2015')

    assert HLOM_Record(record).date == '2015'
