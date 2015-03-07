

from osp.corpus.models.document import Document
from osp.corpus.models.format import Document_Format
from osp.corpus.jobs.format import format


def test_format(models, mock_corpus):

    """
    format() should write the format to the `document_format` table.
    """

    # Add a file, create a document row.
    path = mock_corpus.add_file()
    document = Document.create(path=path)

    format(document.id)

    # Pop out the new row.
    row = Document_Format.get(Document_Format.document==document)
    assert row.format == 'text/plain'
