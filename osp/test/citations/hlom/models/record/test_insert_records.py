

from osp.citations.hlom.models.record import HLOM_Record
from osp.test.citations.hlom.mock_hlom import get_marc


def test_insert_records(models, mock_hlom):

    """
    HLOM_Record.insert_records() should create a row for each MARC record.
    """

    records = []

    # 10 segments:
    for i in range(10):
        with mock_hlom.writer(str(i)+'.dat') as writer:

            # 10 records in each:
            for j in range(10):

                # Create a MARC record.
                cn = str(i)+'-'+str(j)
                marc = get_marc(cn, 'title'+cn, 'author'+cn)

                writer.write(marc)
                records.append(marc)

    HLOM_Record.insert_records()

    # Should insert 100 records.
    assert HLOM_Record.select().count() == 100

    for record in records:
        num = record['001'].format_field()
        row = HLOM_Record.get(HLOM_Record.control_number==num)
        assert row.pymarc.as_marc() == record.as_marc()
