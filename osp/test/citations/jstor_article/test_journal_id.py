

from osp.citations.jstor_article import JSTOR_Article


def test_journal_id(mock_jstor):

    path = mock_jstor.add_article(journal_id='journalname')

    assert JSTOR_Article(path).journal_id == 'journalname'
