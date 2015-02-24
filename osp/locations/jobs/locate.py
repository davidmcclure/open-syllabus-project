

from osp.common.models.base import redis
from osp.corpus.syllabus import Syllabus
from osp.corpus.corpus import Corpus
from osp.corpus.models.document import Document
from osp.institutions.models.institution import Institution
from osp.locations.models.doc_inst import Document_Institution
from rq import Queue


def locate(id):

    """
    Find an institution with the same base URL as a document.

    :param id: The document id.
    """

    doc = Document.get(Document.id==id)

    # Break if no manifest.
    if not doc.syllabus.registered_domain:
        return

    # Form the domain query.
    q = '%'+doc.syllabus.registered_domain+'%'

    match = (
        Institution
        .select()
        .where(Institution.metadata['Institution_Web_Address'] ** (q))
        .order_by(Institution.id)
        .first()
    )

    if match:

        Document_Institution.create(
            institution=match,
            document=doc.id
        )


def queue_locate(s1=0, s2=4095):

    """
    Queue text extraction tasks in the worker.

    :param s1: The first segment.
    :param s2: The last segment.
    """

    queue = Queue(connection=redis)

    for syllabus in Corpus.from_env(s1=s1, s2=s2).syllabi():
        queue.enqueue(locate, syllabus.path)
