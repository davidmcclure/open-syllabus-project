

from osp.corpus.models.document import Document
from osp.locations.models.doc_inst import Document_Institution as DocInst
from osp.institutions.models.institution import Institution
from osp.institutions.models.lonlat import Institution_LonLat as LonLat
from peewee import *


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
        .switch(Institution)
        .join(LonLat)
        .where(~(Document.stored_id >> None))
        .distinct([DocInst.document])
        .order_by(
            DocInst.document,
            DocInst.created.desc()
        )
    )
