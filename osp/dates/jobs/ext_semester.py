

import re

from osp.corpus.models.text import Document_Text
from osp.dates.models.semester import Document_Date_Semester
from datetime import date


def ext_semester(id):

    """
    Try to find a "Spring/Fall YY/YYY" pattern.

    Args:
        id (int): The document id.
    """

    doc = Document_Text.get(Document_Text.id==id)

    pattern = re.compile(r'''
        (?P<semester>fall|spring)
        \s+
        (?P<year>\d{4})
    ''', re.I+re.X)

    match = re.search(pattern, doc.text)

    if match:

        semester = match.group('semester').lower()
        year = int(match.group('year'))

        if semester == 'fall':
            month = 9
        elif semester == 'spring':
            month = 1

        Document_Date_Semester.create(
            document=doc,
            date=date(year, month, 1),
            offset=match.start(),
            semester = match.group('semester'),
            year = year
        )
