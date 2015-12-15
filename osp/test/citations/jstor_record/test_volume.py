

from osp.citations.jstor_record import JSTOR_Record


def test_volume(mock_jstor):

    path = mock_jstor.add_article(issue_volume=200)

    assert JSTOR_Record(path).volume == '200'
