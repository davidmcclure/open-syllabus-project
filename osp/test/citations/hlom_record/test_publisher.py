

from osp.citations.hlom_record import HLOM_Record


def test_publisher(mock_hlom):

    record = mock_hlom.add_marc(publisher='Chicago Press')

    assert HLOM_Record(record).publisher == 'Chicago Press'
