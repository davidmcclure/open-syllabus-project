

from osp.citations.jstor_article import JSTOR_Article


def test_publisher_name(mock_jstor):
    path = mock_jstor.add_article(publisher_name='Publisher Name')
    assert JSTOR_Article(path).publisher_name == 'Publisher Name'
