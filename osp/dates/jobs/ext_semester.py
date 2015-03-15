

import re

from osp.corpus.models.text import Document_Text
from osp.dates.models.semester import Document_Date_Semester
from datetime import datetime


def ext_semester(id):

    """
    Try to find a "Spring/Fall YY/YYY" pattern.

    Args:
        id (int): The document id.
    """

    doc = Document_Text.get(Document_Text.id==id)

    pattern = re.compile(r'''
        (?P<semester>fall|winter|spring|summer)
        [\s\']+
        (?P<year>\d{4}|\d{2})
    ''', re.I+re.X)

    match = re.search(pattern, doc.text)

    if match:

        row = Document_Date_Semester(
            document=doc,
            offset=match.start(),
            semester=match.group('semester'),
            year=match.group('year')
        )

        if row.date.year > 1980 and row.date < datetime.now():
            row.save()
