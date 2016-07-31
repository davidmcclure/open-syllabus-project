

import pytest

from osp.common.utils import parse_domain


@pytest.mark.parametrize('url,domain', [

    # Unchanged
    (
        'test.edu',
        'test.edu',
    ),

    # Strip protocol
    (
        'http://test.edu',
        'test.edu',
    ),
    (
        'https://test.edu',
        'test.edu',
    ),

    # Stip www subdomain
    (
        'www.test.edu',
        'test.edu',
    ),

    # Keep non-www subdomain
    (
        'sub.test.edu',
        'sub.test.edu',
    ),
    (
        'sub1.sub2.test.edu',
        'sub1.sub2.test.edu',
    ),

    # Strip path
    (
        'http://test.edu/syllabus.pdf',
        'test.edu',
    ),

    # Strip whitespace
    (
        '  http://test.edu  ',
        'test.edu',
    ),

    # Downcase
    (
        'WWW.TEST.EDU',
        'test.edu',
    ),

    # Take second domain in embedded URLs
    (
        'https://web.archive.org/123/http:/test.edu/syllabus.pdf',
        'test.edu',
    ),
    (
        'https://web.archive.org/123/https:/test.edu/syllabus.pdf',
        'test.edu',
    ),

])
def test_parse_domain(url, domain):
    assert parse_domain(url) == domain
