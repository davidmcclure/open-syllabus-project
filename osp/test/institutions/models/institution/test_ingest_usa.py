

from osp.institutions.models import Institution


def test_insert_rows():

    """
    Institution.ingest_usa() should load rows.
    """

    Institution.ingest_usa(
        'osp.test.institutions.models.institution',
        'fixtures/ingest_usa/insert_rows.csv',
    )

    assert Institution.select().count() == 3

    for i in map(str, [1, 2, 3]):

        assert Institution.select().where(
            Institution.name=='inst'+i,
            Institution.domain=='inst'+i+'.edu',
            Institution.state=='ST'+i,
            Institution.country=='US',
        )
