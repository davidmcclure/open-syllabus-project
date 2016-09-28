

from osp.citations.hlom_record import HLOM_Record


def test_title(mock_hlom):

    record = mock_hlom.add_marc(title='Book Title')

    assert HLOM_Record(record).title() == 'Book Title'
