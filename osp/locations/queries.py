

from osp.corpus.models.document import Document
from osp.institutions.models.institution import Institution
from peewee import *

from osp.locations.models.document_institution \
    import DocumentInstitution as DocInst


def document_objects():

    """
    Get document -> institution IDs for Overview document-objects.
    """

    iid = Institution.stored_id.alias('iid')
    did = Document.stored_id.alias('did')

    return (
        DocInst
        .select(iid, did)
        .join(Institution)
        .join(Document, on=(DocInst.document==Document.path))
        .where(~(Document.stored_id >> None))
        .distinct([DocInst.document])
        .order_by(
            DocInst.document,
            DocInst.created.desc()
        )
    )
