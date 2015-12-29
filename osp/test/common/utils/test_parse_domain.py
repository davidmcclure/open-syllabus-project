

import pytest

from osp.common.utils import parse_domain


@pytest.mark.parametrize('url,domain', [

    # Unchanged:
    ('test.edu', 'test.edu'),

    # Strip protocol:
    ('http://test.edu', 'test.edu'),

    # Strip subdomain:
    ('www.test.edu', 'test.edu'),
    ('www.sub.test.edu', 'test.edu'),

    # Downcase:
    ('WWW.TEST.EDU', 'test.edu'),

    # Strip whitespace:
    ('  http://test.edu  ', 'test.edu'),

])
def test_parse_domain(url, domain):
    assert parse_domain(url) == domain
