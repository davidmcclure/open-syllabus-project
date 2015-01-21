

import re

from osp.dates.semester.models.semester import Document_Semester
from osp.corpus.queries import document_text


def ext_semester(path):

    """
    Extract a "Fall|Spring YYYY" semester.

    :param str path: The document path.
    """

    text = document_text(path).text

    pattern = re.compile(r'''
        (?P<semester>fall|winter|spring|summer)
        \s+
        (?P<year>\d{4})
    ''', re.I+re.X)

    matches = [m for m in re.finditer(pattern, text)]

    if len(matches):

        match = matches[0]

        Document_Semester.create(
            document=path,
            offset=match.start(),
            semester=match.group('semester').lower(),
            year=match.group('year')
        )
