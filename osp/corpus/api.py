

from osp.common.models.base import queue
from osp.corpus.corpus import Corpus
from osp.corpus.jobs.text import text as job
from flask import Flask, Blueprint, request


corpus = Blueprint('corpus', __name__)


@corpus.route('/text', methods=['POST'])
def text():

    o1 = int(request.form['o1'])
    o2 = int(request.form['o2'])
    job = queue.enqueue(queue_text, o1, o2, timeout=3600)

    code = 200 if job.is_queued else 500
    return ('', 200)


def queue_text(o1, o2):

    """
    Queue text extraction tasks in the worker.

    Args:
        o1 (int): The first id.
        o2 (int): The second id.
    """

    for i in range(o1, o2+1):
        queue.enqueue(job, i)
