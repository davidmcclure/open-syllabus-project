

from osp.citations.jstor_article import JSTOR_Article


def test_volume(mock_jstor):

    path = mock_jstor.add_article(issue_number=10)

    assert JSTOR_Article(path).issue == '10'
