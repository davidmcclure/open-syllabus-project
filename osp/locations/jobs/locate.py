

from osp.corpus.syllabus import Syllabus
from osp.institutions.models.institution import Institution
from osp.locations.models.doc_to_inst import DocToInst


def locate(path):

    """
    Find an institution with the same base URL as a document.

    :param str path: The document path.
    """

    syllabus = Syllabus(path)

    # Break if no manifest.
    if not syllabus.registered_domain:
        return

    # Form the domain query.
    q = '%'+syllabus.registered_domain+'%'

    match = (
        Institution
        .select()
        .where(Institution.metadata['Institution_Web_Address'] ** (q))
        .first()
    )

    if match:

        # Write the association.
        doc2inst = DocToInst(
            institution=match, document=syllabus.uid
        )

        doc2inst.save()
