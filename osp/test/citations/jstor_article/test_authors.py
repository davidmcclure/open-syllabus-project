

import datetime

from osp.citations.jstor_article import JSTOR_Article


def test_pub_date(mock_jstor):

    path = mock_jstor.add_article(authors=[
        ('David', 'McClure'),
        ('Joe', 'Karaganis'),
        ('Dennis', 'Tenen'),
        ('Alex', 'Gil'),
    ])

    assert JSTOR_Article(path).authors == [
        'David McClure',
        'Joe Karaganis',
        'Dennis Tenen',
        'Alex Gil',
    ]
