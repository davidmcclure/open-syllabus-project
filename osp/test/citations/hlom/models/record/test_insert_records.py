

from osp.citations.hlom.models.record import HLOM_Record


def test_insert_records(models, mock_hlom):

    """
    HLOM_Record.insert_records() should create a row for each MARC record.
    """

    records = []

    # 10 segments:
    for i in range(10):

        # 10 records in each:
        for j in range(10):
            marc = mock_hlom.add_marc(data_file=str(i))
            records.append(marc)

    # Insert record rows.
    HLOM_Record.insert_records()

    # Should insert 100 records.
    assert HLOM_Record.select().count() == 100

    for marc in records:

        # Pop out the `hlom_record` row.
        cn = marc['001'].format_field()
        row = HLOM_Record.get(HLOM_Record.control_number==cn)

        # Should store the record body.
        assert row.pymarc.as_marc() == marc.as_marc()
