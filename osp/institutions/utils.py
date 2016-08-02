

import tldextract
import re

from urllib.parse import urlparse


def seed_to_regex(seed):

    """
    Given a URL, make a regex that matches child URLs.

    Args:
        seed (str)

    Returns: regex
    """

    parsed = urlparse(seed)

    # 1 -- If the seed has a non-www subdomain, require a matching subdomain.

    subdomain = ''

    tld = tldextract.extract(seed)

    if tld.subdomain and tld.subdomain != 'www':
        subdomain = '[./]'+tld.subdomain

    # 3 -- yale.edu

    netloc = '[./]{0}.{1}'.format(tld.domain, tld.suffix)

    # 3 -- If a path is present, require a sub-path.

    path = ''

    clean_path = parsed.path.rstrip('/')

    if clean_path:
        path = re.escape(clean_path+'/')

    # Join the parts.

    pattern = ''.join([subdomain, netloc, path])

    return re.compile(pattern, re.I)


def strip_csv_row(row):

    """
    Strip values in a CSV row, casing '' -> None.
    """

    return {
        key: val.strip() or None
        for key, val in row.items()
    }
