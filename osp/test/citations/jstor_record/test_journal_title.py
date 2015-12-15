

from osp.citations.jstor_record import JSTOR_Record


def test_journal_title(mock_jstor):

    path = mock_jstor.add_article(journal_title='Journal Title')

    assert JSTOR_Record(path).journal_title == 'Journal Title'
