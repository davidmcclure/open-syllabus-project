

from osp.citations.jstor_record import JSTOR_Record


def test_article_id(mock_jstor):

    path = mock_jstor.add_article(article_id='12345')

    assert JSTOR_Record(path).article_id == '12345'
