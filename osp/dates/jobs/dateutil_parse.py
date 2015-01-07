

from osp.dates.models.dateutil_parse import DateutilParse
from dateutil.parser import parser


def dateutil_parse(path, text, depth):

    """
    Get a date out of the first X characters with `dateutil.parser`.

    :param str path: The document path.
    :param str text: The document text.
    :param int depth: The number of characters to skim off.
    """

    try:

        date = parser.parse(text[:depth], fuzzy=True)
        DateutilParse.create(document=path, date=date, depth=depth)

    except: pass
