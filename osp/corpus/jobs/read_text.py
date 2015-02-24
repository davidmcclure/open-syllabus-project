

from osp.common.models.base import redis
from osp.corpus.syllabus import Syllabus
from osp.corpus.models.document import Document
from osp.corpus.models.text import Document_Text
from osp.corpus.corpus import Corpus
from rq import Queue


def read_text(id):

    """
    Write the document as plain text.

    :param path: The document id.
    """

    doc = Document.get(Document.id==id)

    if doc.syllabus.text:

        Document_Text.create(
            text=doc.syllabus.unbroken_text,
            document=doc.id
        )


def queue_read_text(s1, s2):

    """
    Queue text extraction tasks in the worker.

    :param s1: The first segment.
    :param s2: The last segment.
    """

    queue = Queue(connection=redis)

    for syllabus in Corpus.from_env(s1=s1, s2=s2).syllabi():
        queue.enqueue(read_text, syllabus.path)
