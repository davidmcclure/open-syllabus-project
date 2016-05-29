

import pytest

from osp.models import Document
from osp.test.utils import segment_range


pytestmark = pytest.mark.usefixtures('db2')


def test_insert_documents(mock_osp, config):

    """
    Corpus.insert_documents() should create a row for each syllabus.
    """

    # 10 segments x 10 files.
    for s in segment_range(10):
        for i in range(10):
            mock_osp.add_file(segment=s, name=s+'-'+str(i))

    Document.ingest()

    with config.transaction() as session:

        # Should create 100 rows.
        assert session.query(Document).count() == 100

        for s in segment_range(10):
            for i in range(10):

                path = s+'/'+s+'-'+str(i)

                # Should create a row for each document.
                query = session.query(Document).filter(Document.path==path)
                assert query.count() == 1


def test_merge_new_documents(mock_osp, config):

    """
    When new documents are added to the corpus, just the new documents should
    be registered in the database.
    """

    # 10 files in 000.
    for i in range(10):
        mock_osp.add_file(segment='000', name='000-'+str(i))

    Document.ingest()

    with config.transaction() as session:

        # Should add 10 initial docs.
        assert session.query(Document).count() == 10

        # 10 new files in 001.
        for i in range(10):
            mock_osp.add_file(segment='001', name='001-'+str(i))

        Document.ingest()

        # Should merge 10 new docs.
        assert session.query(Document).count() == 20
