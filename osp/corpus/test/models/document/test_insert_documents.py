

from osp.common.config import config
from osp.corpus.corpus import Corpus
from osp.corpus.models.document import Document
from osp.corpus.utils import int_to_dir
from playhouse.test_utils import test_database


def test_insert_documents(mock_corpus):

    """
    Corpus.insert_documents()
    """

    # Add 10 segments.
    mock_corpus.add_segments(s1=0, s2=10)

    # Add 10 files per segment.
    for i in range(0, 10):
        segment = int_to_dir(i)
        mock_corpus.add_files(segment, 10, prefix=segment+'-')

    with test_database(config.get_db('test'), (Document,)):

        # Insert document rows.
        corpus = Corpus(mock_corpus.path)
        Document.insert_documents(corpus)

        # Query for the new rows.
        query = Document.select().order_by(Document.id)

        # Should create 100 rows.
        assert query.count() == 100

        # TODO: Check paths.
