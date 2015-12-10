

from osp.citations.models import Text


def test_load_rows(models, mock_hlom):

    """
    Text.ingest_hlom() should ingest HLOM MARC records.
    """

    records = []

    # 10 segments, each with 10 records.
    for i in range(10):
        for j in range(10):
            marc = mock_hlom.add_marc(data_file=str(i))
            records.append(marc)

    Text.ingest_hlom()

    # Should insert 100 records.
    assert Text.select().count() == 100


def test_populate_metadata():
    pass


def test_require_title_and_author():
    pass
