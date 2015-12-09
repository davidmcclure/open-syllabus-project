

from osp.citations.models import Text


def test_insert_records(models, mock_hlom):

    """
    Text.insert_records() should create a row for each MARC record.
    """

    records = []

    # 10 segments:
    for i in range(10):

        # 10 records in each:
        for j in range(10):

            marc = mock_hlom.add_marc(
                data_file=str(i),
                title='title',
                author='author'
            )

            records.append(marc)

    # Insert record rows.
    Text.insert_records()

    # Should insert 100 records.
    assert Text.select().count() == 100

    for marc in records:

        # Pop out the `hlom_record` row.
        row = Text.get(
            Text.control_number==marc.control_number()
        )

        # Should store the record body.
        assert row.marc.as_marc() == marc.as_marc()


def test_require_title_and_author(models, mock_hlom):

    """
    Records that don't have both a title and an author should be ignored.
    """

    # No author, no title:
    m1 = mock_hlom.add_marc(title='', author='')

    # Title, no author:
    m2 = mock_hlom.add_marc(title='War and Peace', author='')

    # Author, no title:
    m3 = mock_hlom.add_marc(title='', author='Leo Tolstoy')

    # Title and author:
    m4 = mock_hlom.add_marc(title='War and Peace', author='Leo Tolstoy')

    Text.insert_records()

    # Should just insert 1 record.
    assert Text.select().count() == 1

    # Should insert the record with title/author.
    assert Text.get(
        Text.control_number==m4.control_number()
    )
