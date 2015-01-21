

import re

from osp.dates.semester.models.semester import Document_Semester
from osp.corpus.queries import document_text


def ext_semester(path):

    """
    Extract a "Fall|Spring YYYY" semester.

    :param str path: The document path.
    """

    text = document_text(path)

    pattern = re.compile(r'''
        (?P<semester>fall|winter|spring|summer)
        \s+
        (?P<year>\d{4}|\d{2})
    ''', re.I+re.X)

    matches = [m.groupdict() for m in re.finditer(pattern, text)]

    if len(matches):

        Document_Semester.create(
            document=path,
            semester=matches[0]['semester'].lower(),
            year=matches[0]['year']
        )
