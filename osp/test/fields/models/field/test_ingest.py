

from osp.fields.models import Field


def test_ingest(models):

    """
    Field.ingest() should load rows from a CSV.
    """

    Field.ingest(
        'osp.test.fields.models.field',
        'fixtures/ingest/ingest.csv',
    )

    assert Field.select().count() == 3

    assert Field.select().where(Field.name=='Field1')
    assert Field.select().where(Field.name=='Field2')
    assert Field.select().where(Field.name=='Field3')
