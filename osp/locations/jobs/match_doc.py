

from osp.corpus.models.document import Document
from osp.institutions.models.institution import Institution
from osp.locations.models.doc_inst import Document_Institution


def match_doc(id):

    """
    Find an institution with the same base URL as a document.

    Args:
        id (int): A document id.
    """

    doc = Document.get(Document.id==id)

    # Break if no manifest.
    if not doc.syllabus.registered_domain:
        return

    # Form the domain query.
    q = '%'+doc.syllabus.registered_domain+'%'

    inst = (
        Institution
        .select()
        .where(Institution.metadata['Institution_Web_Address'] ** (q))
        .order_by(Institution.id)
        .first()
    )

    if inst:

        Document_Institution.create(
            document=doc.id,
            institution=inst
        )
