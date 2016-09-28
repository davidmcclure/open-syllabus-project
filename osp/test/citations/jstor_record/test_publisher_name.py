

from osp.citations.jstor_record import JSTOR_Record


def test_publisher_name(mock_jstor):

    path = mock_jstor.add_article(publisher_name='Publisher Name')

    assert JSTOR_Record(path).publisher_name() == 'Publisher Name'
