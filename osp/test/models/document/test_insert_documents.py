

import pytest

from osp.models import Document
from osp.test.utils import segment_range


pytestmark = pytest.mark.usefixtures('db2')


# @pytest.mark.skip
def test_insert_documents(mock_osp, config):

    """
    Corpus.insert_documents() should create a row for each syllabus.
    """

    # 10 segments x 10 files.
    for s in segment_range(10):
        for i in range(10):
            mock_osp.add_file(segment=s, name=s+'-'+str(i))

    # Insert document rows.
    Document.insert_documents()

    with config.transaction() as session:

        # Should create 100 rows.
        assert session.query(Document).count() == 100

        # All docs should have rows.
        for s in segment_range(10):
            for i in range(10):

                # [segment]/[file]
                path = s+'/'+s+'-'+str(i)

                # Query for the document path.
                assert (
                    session
                    .query(Document)
                    .filter(Document.path==path).count()
                ) == 1


@pytest.mark.skip
def test_insert_new_documents(mock_osp):

    """
    When new documents are added to the corpus, just the new documents should
    be registered in the database.
    """

    # 10 files in `000`.
    for i in range(10):
        mock_osp.add_file(segment='000', name='000-'+str(i))

    # Should add 10 docs.
    Document.insert_documents()
    assert Document.select().count() == 10

    # 10 new files in `001`.
    for i in range(10):
        mock_osp.add_file(segment='001', name='001-'+str(i))

    # Should add 10 docs.
    Document.insert_documents()
    assert Document.select().count() == 20
