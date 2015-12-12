

import datetime

from osp.citations.jstor_article import JSTOR_Article


def test_pub_date(mock_jstor):

    path = mock_jstor.add_article(pub_year=1987, pub_month=6, pub_day=25)

    date = datetime.date(1987, 6, 25)

    assert JSTOR_Article(path).pub_date == date.isoformat()
