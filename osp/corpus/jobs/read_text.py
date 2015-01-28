

from osp.common.models.base import redis
from osp.corpus.syllabus import Syllabus
from osp.corpus.models.text import Document_Text
from osp.corpus.corpus import Corpus
from rq import Queue


def read_text(path):

    """
    Write the document as plaintext.

    :param str path: The document path.
    """

    syllabus = Syllabus(path)

    if syllabus.text:

        Document_Text.create(
            text=syllabus.unbroken_text,
            document=syllabus.relative_path
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


def queue(s1, s2):
    queue = Queue(connection=redis)
    queue.enqueue(queue_read_text, s1, s2, timeout=3600)
