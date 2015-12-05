

import tldextract


def parse_domain(url):

    """
    Extract a domain from a URL.

    Args:
        url (str)
    """

    return tldextract.extract(url).registered_domain.lower()
