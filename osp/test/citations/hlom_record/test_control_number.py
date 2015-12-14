

from osp.citations.hlom_record import HLOM_Record


def test_control_number(mock_hlom):

    record = mock_hlom.add_marc(control_number='001')

    assert HLOM_Record(record).control_number == '001'
