

from osp.corpus.models.document import Document
from osp.corpus.models.format import Document_Format
from osp.corpus.jobs.read_format import read_format


def test_read_format(models, mock_corpus):

    """
    read_format() should write the format to the `document_format` table.
    """

    # Add a file, create a document row.
    path = mock_corpus.add_file()
    document = Document.create(path=path)

    read_format(document.id)

    # Pop out the new row.
    row = Document_Format.get(Document_Format.document==document)
    assert row.format == 'text/plain'
