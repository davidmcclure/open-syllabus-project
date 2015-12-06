

from osp.institutions.models import Institution
from osp.institutions.models import Institution_Document
from osp.corpus.models import Document


def doc_to_inst(doc_id):

    """
    Match a document with an institution.
    """

    doc = Document.get(Document.id==doc_id)

    inst = (
        Institution
        .select()
        .where(Institution.domain==doc.syllabus.domain)
        .first()
    )

    if inst:

        Institution_Document.create(
            institution=inst,
            document=doc,
        )
