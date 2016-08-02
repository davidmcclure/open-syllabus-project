

import pytest
import re

from osp.institutions.utils import seed_to_regex


@pytest.mark.parametrize('seed,url,result', [

    # Match URLs that are "below" the seed path.
    (
        'http://yale.edu',
        'http://yale.edu/page',
        True,
    ),
    (
        'http://yale.edu/root',
        'http://yale.edu/root/page',
        True,
    ),
    (
        'http://yale.edu/root',
        'http://yale.edu/root/page.html',
        True,
    ),

    # Don't match URLs that are adjacent to or above the seed path.
    (
        'http://yale.edu/root1',
        'http://yale.edu/root2',
        False,
    ),
    (
        'http://yale.edu/root1/root2',
        'http://yale.edu/root1',
        False,
    ),
    (
        'http://yale.edu/root',
        'http://yale.edu/root2/page',
        False,
    ),

    # When the seed has no subdomain (or just www), match any subdomain.
    (
        'http://yale.edu',
        'http://sub.yale.edu',
        True,
    ),
    (
        'http://www.yale.edu',
        'http://sub.yale.edu',
        True,
    ),

    # When the seed has a non-www subdomain, the URL must have the exact same
    # subdomain as the seed.
    (
        'http://sub.yale.edu',
        'http://sub.yale.edu',
        True,
    ),
    (
        'http://sub1.yale.edu',
        'http://sub2.yale.edu',
        False,
    ),

    # Match URLs with the same subdomain with additional subdomains.
    (
        'http://sub1.yale.edu',
        'http://sub2.sub1.yale.edu',
        True,
    ),

    # Ignore casing.
    (
        'http://yale.edu',
        'http://YALE.EDU',
        True,
    ),

    # Don't match URLs with different hosts.
    (
        'http://yale.edu',
        'http://harvard.edu',
        False,
    ),

    # Match different protocols.
    (
        'http://yale.edu',
        'https://yale.edu',
        True,
    ),
    (
        'https://yale.edu',
        'http://yale.edu',
        True,
    ),

    # Ignore trailing slash on path.
    (
        'http://yale.edu/',
        'http://yale.edu/page',
        True,
    ),
    (
        'http://yale.edu/root/',
        'http://yale.edu/root/page',
        True,
    ),

    # Match embedded child URLs.
    (
        'http://yale.edu',
        'http://web.archive.org/123/http:/yale.edu/syllabus.pdf',
        True,
    ),
    (
        'http://yale.edu',
        'http://web.archive.org/123/yale.edu/syllabus.pdf',
        True,
    ),

    # Don't match embedded non-child URLs.
    (
        'http://yale.edu/root1',
        'http://web.archive.org/123/http:/yale.edu/root2',
        False,
    ),

    # Don't match "superset" netlocs or subdomains, where the document value
    # ends with the seed value but isn't the same.
    (
        'http://su.edu/',
        'http://wsu.edu/syllabus.pdf',
        False,
    ),
    (
        'http://lit.yale.edu/',
        'http://complit.yale.edu/syllabus.pdf',
        False,
    ),

])
def test_seed_to_regex(seed, url, result):

    r = seed_to_regex(seed)

    assert bool(r.search(url)) == result
