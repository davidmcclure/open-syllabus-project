

from osp.citations.jstor_record import JSTOR_Record


def test_article_title(mock_jstor):

    path = mock_jstor.add_article(article_title='Test Title')

    assert JSTOR_Record(path).article_title() == 'Test Title'
