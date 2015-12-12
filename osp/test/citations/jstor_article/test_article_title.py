

from osp.citations.jstor_article import JSTOR_Article


def test_article_title(mock_jstor):

    """
    JSTOR_Article#article_title should pro
    """

    path = mock_jstor.add_article(article_title='Test Title')

    assert JSTOR_Article(path).article_title == 'Test Title'
