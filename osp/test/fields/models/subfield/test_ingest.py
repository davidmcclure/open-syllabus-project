

from osp.fields.models import Field
from osp.fields.models import Subfield


def test_insert_rows(models):

    """
    Subfield.ingest() should load field and subfield rows.
    """

    Subfield.ingest(
        'osp.test.fields.models.subfield',
        'fixtures/ingest/insert_rows.csv',
    )

    assert Field.select().count() == 3
    assert Subfield.select().count() == 9

    f1 = Field.get(Field.name=='Field1')
    f2 = Field.get(Field.name=='Field2')
    f3 = Field.get(Field.name=='Field3')

    sf1 = Subfield.get(Subfield.name=='Subfield1')
    sf2 = Subfield.get(Subfield.name=='Subfield2')
    sf3 = Subfield.get(Subfield.name=='Subfield3')
    sf4 = Subfield.get(Subfield.name=='Subfield4')
    sf5 = Subfield.get(Subfield.name=='Subfield5')
    sf6 = Subfield.get(Subfield.name=='Subfield6')
    sf7 = Subfield.get(Subfield.name=='Subfield7')
    sf8 = Subfield.get(Subfield.name=='Subfield8')
    sf9 = Subfield.get(Subfield.name=='Subfield9')

    assert sf1.field == f1
    assert sf2.field == f1
    assert sf3.field == f1

    assert sf4.field == f2
    assert sf5.field == f2
    assert sf6.field == f2

    assert sf7.field == f3
    assert sf8.field == f3
    assert sf9.field == f3


def test_clean_field_names(models):

    """
    Field and subfield names should be sanitized.
    """

    Subfield.ingest(
        'osp.test.fields.models.subfield',
        'fixtures/ingest/clean_field_names.csv',
    )

    assert Field.select().where(Field.name=='Field1')

    assert Subfield.select().where(Subfield.name=='Subfield1')
    assert Subfield.select().where(Subfield.name=='Subfield2')
    assert Subfield.select().where(Subfield.name=='Subfield3')


def test_parse_abbrs(models):

    """
    Abbreviations should be parsed.
    """

    Subfield.ingest(
        'osp.test.fields.models.subfield',
        'fixtures/ingest/parse_abbrs.csv',
    )

    sf1 = Subfield.get(Subfield.name=='Subfield1')
    sf2 = Subfield.get(Subfield.name=='Subfield2')
    sf3 = Subfield.get(Subfield.name=='Subfield3')

    assert sf1.abbreviations == ['AB1', 'AB2']
    assert sf2.abbreviations == ['AB3', 'AB4']
    assert sf3.abbreviations == ['AB5', 'AB6']


def test_filter_abbrs(models):

    """
    Blacklisted abbreviations should be filtered out.
    """

    Subfield.ingest(
        'osp.test.fields.models.subfield',
        'fixtures/ingest/filter_abbrs.csv',
    )

    sf1 = Subfield.get(Subfield.name=='Subfield1')
    sf2 = Subfield.get(Subfield.name=='Subfield2')
    sf3 = Subfield.get(Subfield.name=='Subfield3')

    assert sf1.abbreviations == ['SF1']
    assert sf2.abbreviations == ['SF2']
    assert sf3.abbreviations == ['SF3']
