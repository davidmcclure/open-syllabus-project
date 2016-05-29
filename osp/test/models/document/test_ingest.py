

import pytest

from osp.models import Document
from osp.corpus.syllabus import Syllabus
from osp.test.utils import segment_range


pytestmark = pytest.mark.usefixtures('db2')


def test_insert_documents(mock_osp, config):

    """
    Corpus.insert_documents() should create a row for each syllabus.
    """

    # 10 segments X 10 files.
    paths = [
        mock_osp.add_file(segment=s, name=str(i))
        for s in segment_range(10)
        for i in range(10)
    ]

    Document.ingest()

    with config.transaction() as session:

        # Should create 100 rows.
        assert session.query(Document).count() == 100

        for path in paths:

            s = Syllabus(path)

            assert (
                session.query(Document)
                .filter(Document.path==s.relative_path)
                .count()
            ) == 1


def test_merge_new_documents(mock_osp, config):

    """
    When new documents are added to the corpus, just the new documents should
    be registered in the database.
    """

    # 10 files in 000.
    paths000 = [
        mock_osp.add_file(segment='000', name=str(i))
        for i in range(10)
    ]

    Document.ingest()

    # 10 new files in 001.
    paths001 = [
        mock_osp.add_file(segment='001', name=str(i))
        for i in range(10)
    ]

    Document.ingest()

    with config.transaction() as session:

        # Just 20 total documents.
        assert session.query(Document).count() == 20

        for path in paths000 + paths001:

            s = Syllabus(path)

            assert (
                session.query(Document)
                .filter(Document.path==s.relative_path)
                .count()
            ) == 1
