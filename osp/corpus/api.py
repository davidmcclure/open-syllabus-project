

from osp.common.models.base import redis
from osp.corpus.corpus import Corpus
from osp.corpus.jobs.text import text
from flask import Flask, Blueprint, request
from rq import Queue


corpus = Blueprint('corpus', __name__)


@corpus.route('/text', methods=['POST'])
def text():

    o1 = int(request.form['o1'])
    o2 = int(request.form['o2'])

    queue = Queue(connection=redis)
    job = queue.enqueue(queue_text, o1, o2, timeout=3600)

    code = 200 if job.is_queued else 500
    return ('', 200)


def queue_text(o1, o2):

    """
    Queue text extraction tasks in the worker.

    :param o1: The first id.
    :param o2: The last id.
    """

    queue = Queue(connection=redis)

    for i in range(o1, o2+1):
        queue.enqueue(read_text, i)
