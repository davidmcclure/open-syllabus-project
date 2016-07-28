

import pytest
import re

from osp.institutions.utils import seed_to_regex


@pytest.mark.parametrize('seed,url,result', [

    # Allow URLs that are "below" the seed path.
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

    # Block URLs that are adjacent to or above the seed path.
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

    # When the seed has no subdomain (or just www), allow any subdomain.
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
    (
        'http://sub1.yale.edu',
        'http://sub2.sub1.yale.edu',
        False,
    ),

    # Ignore casing.
    (
        'http://yale.edu',
        'http://YALE.EDU',
        True,
    ),

    # Block URLs with different hosts.
    (
        'http://yale.edu',
        'http://harvard.edu',
        False,
    ),

    # Allow different protocols.
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

    # Block embedded non-child URLs.
    (
        'http://yale.edu/root1',
        'http://web.archive.org/123/http:/yale.edu/root2',
        False,
    ),

])
def test_seed_to_regex(seed, url, result):

    r = seed_to_regex(seed)

    assert bool(r.search(url)) == result
