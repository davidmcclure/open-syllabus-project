

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
        (?P<semester>fall|spring)
        [\s\']+
        (?P<year>\d{4}|\d{2})
    ''', re.I+re.X)

    match = re.search(pattern, doc.text)

    if match:

        year = match.group('year')

        # Get the year.
        if len(year) == 4:
            date = datetime.strptime(year, '%Y')
        elif len(year) == 2:
            date = datetime.strptime(year, '%y')

        semester = match.group('semester').lower()

        # Get the month.
        if semester == 'spring':
            month = 1
        elif semester == 'fall':
            month = 9

        # Set the month.
        date = date.replace(month=month)

        if date.year > 1980 and date < datetime.now():

            Document_Date_Semester.create(
                document=doc,
                offset=match.start(),
                date=date
            )
