

import datetime
import pytest

from osp.citations.jstor_record import JSTOR_Record


@pytest.mark.parametrize('year,month,day,date', [

    (1987, 6, 25, datetime.date(1987, 6, 25).isoformat()),

    # Empty components.
    ('', 6, 25, None),
    (1987, '', 25, None),
    (1987, 6, '', None),

    # Missing components.
    (None, 6, 25, None),
    (1987, None, 25, None),
    (1987, 6, None, None),

])
def test_pub_date(year, month, day, date, mock_jstor):

    path = mock_jstor.add_article(
        pub_year=year,
        pub_month=month,
        pub_day=day,
    )

    assert JSTOR_Record(path).pub_date == date
