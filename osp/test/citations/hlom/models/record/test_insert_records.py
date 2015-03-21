

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

            cn = str(i)+'-'+str(j)

            marc = mock_hlom.add_marc(
                data_file=str(i),
                control_number=cn
            )

            records.append((marc, cn))

    # Insert record rows.
    HLOM_Record.insert_records()

    # Should insert 100 records.
    assert HLOM_Record.select().count() == 100

    # Should store the records.
    for marc, cn in records:
        row = HLOM_Record.get(HLOM_Record.control_number==cn)
        assert row.pymarc.as_marc() == marc.as_marc()
