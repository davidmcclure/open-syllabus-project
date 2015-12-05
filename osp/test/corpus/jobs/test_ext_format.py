

from osp.corpus.models.document import Document
from osp.corpus.models.document_format import Document_Format
from osp.corpus.jobs.ext_format import ext_format


def test_read_format(models, mock_osp):

    """
    read_format() should write the format to the `document_format` table.
    """

    # Add a file, create a document row.
    path = mock_osp.add_file()
    document = Document.create(path=path)

    ext_format(document.id)

    # Pop out the new row.
    row = Document_Format.get(Document_Format.document==document)
    assert row.format == 'text/plain'
