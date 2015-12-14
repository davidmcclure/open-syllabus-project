

from osp.citations.jstor_article import JSTOR_Article


def test_article_id(mock_jstor):

    path = mock_jstor.add_article(article_title='Test Title')

    assert JSTOR_Article(path).article_title == 'Test Title'
