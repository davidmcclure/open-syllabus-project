

import pytest

from osp.institutions.models import Institution


pytestmark = pytest.mark.usefixtures('db')


def test_insert_rows():

    """
    Institution.ingest_world() should load rows.
    """

    Institution.ingest_world(
        'osp.test.institutions.models.institution',
        'fixtures/ingest_world/insert_rows.csv',
    )

    assert Institution.select().count() == 3

    for i in map(str, [1, 2, 3]):

        assert Institution.select().where(
            Institution.name=='inst{0}'.format(i),
            Institution.url=='http://inst{0}.edu'.format(i),
            Institution.state==None,
            Institution.country=='C{0}'.format(i),
        )


def test_skip_us_rows():

    """
    "US" institutions should be ignored.
    """

    Institution.ingest_world(
        'osp.test.institutions.models.institution',
        'fixtures/ingest_world/skip_us_rows.csv',
    )

    assert Institution.select().count() == 2

    assert Institution.select().where(Institution.name=='inst1')
    assert Institution.select().where(Institution.name=='inst2')
    assert not Institution.select().where(Institution.name=='inst3')


def test_strip_values():

    """
    Field values should be stripped.
    """

    Institution.ingest_world(
        'osp.test.institutions.models.institution',
        'fixtures/ingest_world/strip_values.csv',
    )

    assert Institution.select().where(
        Institution.name=='inst',
        Institution.url=='http://inst.edu',
        Institution.state==None,
        Institution.country=='AU',
    )
