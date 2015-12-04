

import re

from osp.corpus.models.text import Document_Text
from osp.fields.models.field import Field
from osp.fields.models.field_document import Field_Document


def ext_fields(doc_id, radius=100):

    """
    Search for field / department codes in a document.

    Args:
        doc_id (int)
        radius (int)
    """

    # Get the document text.
    doc_text = Document_Text.get(Document_Text.document==doc_id)

    # Search for each field.
    for field in Field.select():

        match = field.search(doc_text.text)

        # If found, link field -> doc.
        if match:

            # Slice out the snippet.
            i1 = max(match.start() - radius, 0)
            i2 = min(match.end() + radius, len(doc_text.text))
            snippet = doc_text.text[i1:i2]

            # Replace linebreaks / whitespace.
            snippet = re.sub('\s{2,}', ' ', snippet).strip()

            Field_Document.create(
                field=field,
                document=doc_text.document,
                snippet=snippet,
            )