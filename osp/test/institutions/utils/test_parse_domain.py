

import pytest

from osp.institutions.utils import parse_domain


@pytest.mark.parametrize('url,domain', [
    ('test.edu', 'test.edu'),
    ('http://test.edu', 'test.edu'),
    ('www.test.edu', 'test.edu'),
    ('WWW.TEST.EDU', 'test.edu'),
])
def test_parse_domain(url, domain):
    assert parse_domain(url) == domain
