

import pytest

from osp.corpus.corpus import Corpus
from osp.corpus.models import Document
from osp.test.utils import segment_range


pytestmark = pytest.mark.usefixtures('db')


def test_insert_documents(mock_osp):

    """
    Corpus.insert_documents() should create a row for each syllabus.
    """

    # 10 segments x 10 files.
    for s in segment_range(10):
        for i in range(10):
            mock_osp.add_file(segment=s, name=s+'-'+str(i))

    # Insert document rows.
    Document.insert_documents()

    # Should create 100 rows.
    assert Document.select().count() == 100

    # All docs should have rows.
    for s in segment_range(10):
        for i in range(10):

            # Path is [segment]/[file]
            path = s+'/'+s+'-'+str(i)

            # Query for the document path.
            query = Document.select().where(Document.path==path)
            assert query.count() == 1


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
