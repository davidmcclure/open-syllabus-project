

from bs4 import BeautifulSoup


def requires_attr(attr):

    """
    If the instance doesn't have a defined value for a key, return None.

    :param attr: The syllabus path.
    """

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if getattr(self, attr, None):
                return func(self, *args, **kwargs)
            else: return None
        return wrapper
    return decorator


def int_to_dir(i):

    """
    Convert an integer offset to a segment directory name.

    :param i: The integer.
    """

    return hex(i)[2:].zfill(3)


def html_to_text(html, exclude=['script', 'style']):

    """
    Convert HTML to text.

    :param html: The raw HTML.
    """

    soup = BeautifulSoup(html)

    # Stript excluded tags.
    for script in soup(exclude):
        script.extract()

    return soup.get_text()
