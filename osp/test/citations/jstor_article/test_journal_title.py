

from osp.citations.jstor_article import JSTOR_Article


def test_journal_title(mock_jstor):
    path = mock_jstor.add_article(journal_title='Journal Title')
    assert JSTOR_Article(path).journal_title == 'Journal Title'
