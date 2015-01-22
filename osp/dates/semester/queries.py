

from peewee import *
from osp.dates.semester.models.semester import Document_Semester


def semester_counts():

    """
    Map semesters to document counts.
    """

    count = fn.Count(Document_Semester.id)

    return (
        Document_Semester
        .select(
            Document_Semester.year,
            Document_Semester.semester,
            count.alias('count')
        )
        .distinct(Document_Semester.document)
        .group_by(
            Document_Semester.year,
            Document_Semester.semester
        )
        .order_by(count.desc())
    )
