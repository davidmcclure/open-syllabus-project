

from osp.citations.jstor_record import JSTOR_Record


def test_volume(mock_jstor):

    path = mock_jstor.add_article(url='http://www.test.org')

    assert JSTOR_Record(path).url() == 'http://www.test.org'
