

from osp.citations.jstor_record import JSTOR_Record


def test_journal_id(mock_jstor):

    path = mock_jstor.add_article(journal_id='journalname')

    assert JSTOR_Record(path).journal_id() == 'journalname'
