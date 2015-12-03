

from osp.corpus.models.text import Document_Text
from osp.fields.models.field import Field
from osp.fields.models.field_document import Field_Document


def ext_fields(doc_id):

    """
    Search for field / department codes in a document.

    Args:
        doc_id (int): The document id.
    """

    # Get the document text.
    doc_text = Document_Text.get(Document_Text.document==doc_id)

    # Search for each field.
    for field in Field.select():
        if field.search(doc_text.text):

            # If found, link field -> doc.
            Field_Document.create(
                field=field,
                document=doc_text.document
            )
