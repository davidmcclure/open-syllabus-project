

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

    # 1 -- http(s)://

    protocol = '^https?{0}'.format(re.escape('://'))

    # 2 -- If the seed has a non-www subdomain, require a matching subdomain.

    subdomain = '.*'

    tld = tldextract.extract(seed)

    if tld.subdomain and tld.subdomain != 'www':
        subdomain = re.escape(tld.subdomain+'.')

    # 3 -- yale.edu

    netloc = re.escape('.'.join([tld.domain, tld.suffix]))

    # 4 -- If a path is present, require a sub-path.

    path = '.*'

    clean_path = parsed.path.rstrip('/')

    if clean_path:
        path = re.escape(clean_path+'/')

    # Join the parts.

    pattern = ''.join([protocol, subdomain, netloc, path])

    return re.compile(pattern, re.I)
