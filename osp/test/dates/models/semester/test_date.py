

from osp.dates.models.semester import Document_Date_Semester


def test_fall_semester():

    """
    Fall 2012
    """

    row = Document_Date_Semester(semester='Fall', year='2012')

    assert row.date.year == 2012
    assert row.date.month == 9


def test_autumn_semester():

    """
    Autumn 2012
    """

    row = Document_Date_Semester(semester='Autumn', year='2012')

    assert row.date.year == 2012
    assert row.date.month == 9


def test_winter_semester():

    """
    Winter 2012
    """

    row = Document_Date_Semester(semester='Winter', year='2012')

    assert row.date.year == 2012
    assert row.date.month == 1


def test_spring_semester():

    """
    Spring 2012
    """

    row = Document_Date_Semester(semester='Spring', year='2012')

    assert row.date.year == 2012
    assert row.date.month == 1


def test_summer_semester():

    """
    Summer 2012
    """

    row = Document_Date_Semester(semester='Summer', year='2012')

    assert row.date.year == 2012
    assert row.date.month == 6


def test_ignore_case():

    """
    The case of the semester should be ignored
    """

    cases = [
        'Summer',
        'SUMMER',
        'summer',
        'SuMmEr',
    ]

    for semester in cases:

        row = Document_Date_Semester(semester=semester, year='2012')

        assert row.date.year == 2012
        assert row.date.month == 6


def test_two_digit_year():

    """
    Fall 12
    """

    row = Document_Date_Semester(semester='Fall', year='12')

    assert row.date.year == 2012
    assert row.date.month == 9
